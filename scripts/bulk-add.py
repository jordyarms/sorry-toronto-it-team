#!/usr/bin/env python3
"""
Bulk add communities from CSV to Jekyll _communities collection.

Usage:
    python bulk_add_communities.py input.csv [--dry-run] [--source "Custom source"]

CSV Format:
    name,description,link,tags
    "Community Name","Description","https://example.com","tag1,tag2"

Options:
    --dry-run: Show what would be created without actually creating files
    --source: Custom source attribution (default: "bulk import")
    --overwrite: Overwrite existing files with same name
"""

import csv
import os
import sys
import argparse
import re
import yaml
from pathlib import Path
from datetime import datetime


def slugify(text):
    """Convert text to a filename-safe slug."""
    if not text or not text.strip():
        return "community"

    # Convert to lowercase and replace non-alphanumeric with hyphens
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower())
    # Remove leading/trailing hyphens and multiple consecutive hyphens
    slug = re.sub(r"^-+|-+$", "", slug)
    slug = re.sub(r"-+", "-", slug)
    return slug or "community"


def process_tags(tags_str):
    """Process comma-separated tags string into a list."""
    if not tags_str or not isinstance(tags_str, str) or tags_str.strip() == "":
        return []

    # Split by comma and clean up whitespace
    tags = [tag.strip() for tag in tags_str.split(",")]
    # Remove empty tags
    tags = [tag for tag in tags if tag]
    return tags


def validate_url(url):
    """Validate that URL is properly formatted."""
    if not url or not isinstance(url, str):
        return False

    url = url.strip()
    if not url:
        return False

    # Check for valid protocol
    if not (url.startswith("http://") or url.startswith("https://")):
        return False

    # Basic check that there's something after the protocol
    if url in ("http://", "https://"):
        return False

    return True


def create_community_file(
    community_data, communities_dir, dry_run=False, overwrite=False
):
    """Create a markdown file for a community."""
    name = community_data["name"].strip()
    description = community_data.get("description", "").strip()
    link = community_data["link"].strip()
    tags = process_tags(community_data.get("tags", ""))
    source = community_data.get("source", "bulk import").strip()

    # Generate filename
    base_filename = slugify(name)
    filename = f"{base_filename}.md"
    filepath = communities_dir / filename

    # Handle duplicate filenames
    counter = 1
    original_filepath = filepath
    while filepath.exists() and not overwrite:
        filename = f"{base_filename}-{counter}.md"
        filepath = communities_dir / filename
        counter += 1

    # Prepare YAML frontmatter data
    frontmatter_data = {
        "name": name,
        "link": link,
        "description": description,
        "source": source,
        "tags": tags,
    }

    # Generate file content
    try:
        yaml_content = yaml.dump(
            frontmatter_data,
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False,
            default_style='"'
            if any('"' in str(v) for v in frontmatter_data.values())
            else None,
        )
    except Exception as e:
        print(f"✗ Error generating YAML for {name}: {e}")
        return filepath, False

    file_content = f"""---
{yaml_content.rstrip()}
---

<!-- Community added via bulk import -->
"""

    if dry_run:
        print(f"[DRY RUN] Would create: {filepath}")
        print(f"  Name: {name}")
        print(f"  Link: {link}")
        print(f"  Description: {description}")
        print(f"  Tags: {tags}")
        print(f"  Source: {source}")
        if filepath != original_filepath:
            print(f"  Note: Filename adjusted to avoid conflict")
        print()
        return filepath, True
    else:
        try:
            # Ensure parent directory exists
            filepath.parent.mkdir(parents=True, exist_ok=True)

            # Create the file
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(file_content)

            print(f"✓ Created: {filepath}")
            if filepath != original_filepath:
                print(f"  Note: Filename adjusted to avoid conflict")
            return filepath, True
        except Exception as e:
            print(f"✗ Error creating {filepath}: {e}")
            return filepath, False


def validate_csv_row(row, row_num):
    """Validate a CSV row has required fields."""
    errors = []

    # Check for name
    name = row.get("name", "")
    if not name or not isinstance(name, str) or not name.strip():
        errors.append(f"Row {row_num}: Missing or empty 'name' field")

    # Check for link
    link = row.get("link", "")
    if not link or not isinstance(link, str) or not link.strip():
        errors.append(f"Row {row_num}: Missing or empty 'link' field")
    elif not validate_url(link):
        errors.append(f"Row {row_num}: Invalid URL format in 'link' field: {link}")

    # Optional: warn about missing description
    description = row.get("description", "")
    if not description or not description.strip():
        print(f"Warning Row {row_num}: Empty description for '{name}'")

    return errors


def detect_csv_encoding(file_path):
    """Attempt to detect CSV file encoding."""
    encodings_to_try = ["utf-8", "utf-8-sig", "iso-8859-1", "cp1252"]

    for encoding in encodings_to_try:
        try:
            with open(file_path, "r", encoding=encoding) as f:
                f.read()
            return encoding
        except UnicodeDecodeError:
            continue

    return "utf-8"  # fallback


def main():
    parser = argparse.ArgumentParser(description="Bulk add communities from CSV")
    parser.add_argument("csv_file", help="Path to CSV file")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be created without creating files",
    )
    parser.add_argument(
        "--source", default="bulk import", help="Source attribution for all communities"
    )
    parser.add_argument(
        "--overwrite", action="store_true", help="Overwrite existing files"
    )
    parser.add_argument(
        "--communities-dir",
        default="_communities",
        help="Path to communities directory",
    )

    args = parser.parse_args()

    # Validate inputs
    csv_path = Path(args.csv_file)
    if not csv_path.exists():
        print(f"Error: CSV file '{csv_path}' not found")
        sys.exit(1)

    if not csv_path.is_file():
        print(f"Error: '{csv_path}' is not a file")
        sys.exit(1)

    communities_dir = Path(args.communities_dir)
    if not args.dry_run:
        try:
            communities_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            print(
                f"Error: Could not create communities directory '{communities_dir}': {e}"
            )
            sys.exit(1)

    # Detect encoding and read CSV
    encoding = detect_csv_encoding(csv_path)
    print(f"Using encoding: {encoding}")

    try:
        with open(csv_path, "r", encoding=encoding) as csvfile:
            # Detect delimiter
            sample = csvfile.read(1024)
            csvfile.seek(0)

            try:
                sniffer = csv.Sniffer()
                delimiter = sniffer.sniff(sample).delimiter
            except Exception:
                delimiter = ","  # fallback to comma
                print("Warning: Could not detect CSV delimiter, using comma")

            reader = csv.DictReader(csvfile, delimiter=delimiter)

            # Validate required columns
            if not reader.fieldnames:
                print("Error: CSV file appears to be empty or invalid")
                sys.exit(1)

            required_columns = {"name", "link"}
            available_columns = set(reader.fieldnames)

            if not required_columns.issubset(available_columns):
                missing = required_columns - available_columns
                print(f"Error: CSV missing required columns: {missing}")
                print(f"Found columns: {list(reader.fieldnames)}")
                sys.exit(1)

            communities = []
            try:
                communities = list(reader)
            except Exception as e:
                print(f"Error parsing CSV content: {e}")
                sys.exit(1)

    except Exception as e:
        print(f"Error reading CSV file: {e}")
        sys.exit(1)

    if not communities:
        print("No communities found in CSV file")
        sys.exit(0)

    print(f"Found {len(communities)} communities in CSV")
    print(f"Target directory: {communities_dir}")
    print(f"Source attribution: {args.source}")
    if args.dry_run:
        print("DRY RUN MODE - No files will be created")
    print("-" * 50)

    # Validate all rows first
    all_errors = []
    for i, row in enumerate(communities, 1):
        errors = validate_csv_row(row, i)
        all_errors.extend(errors)

    if all_errors:
        print("Validation errors found:")
        for error in all_errors:
            print(f"  {error}")
        print(
            f"\nFound {len(all_errors)} validation errors. Please fix them and try again."
        )
        sys.exit(1)

    # Process communities
    created_files = []
    failed_files = []

    for i, row in enumerate(communities, 1):
        # Add source to community data
        community_data = dict(row)
        community_data["source"] = args.source

        filepath, success = create_community_file(
            community_data,
            communities_dir,
            dry_run=args.dry_run,
            overwrite=args.overwrite,
        )

        if success:
            created_files.append(filepath)
        else:
            failed_files.append(filepath)

    # Summary
    print("-" * 50)
    if args.dry_run:
        print(f"DRY RUN COMPLETE:")
        print(f"  Would create: {len(created_files)} files")
        print(f"  Would fail: {len(failed_files)} files")
    else:
        print(f"BULK IMPORT COMPLETE:")
        print(f"  Successfully created: {len(created_files)} files")
        print(f"  Failed: {len(failed_files)} files")

        if created_files:
            print(f"\nCreated files:")
            for filepath in created_files:
                print(f"  {filepath}")

        if failed_files:
            print(f"\nFailed files:")
            for filepath in failed_files:
                print(f"  {filepath}")

    # Exit with appropriate code
    sys.exit(0 if len(failed_files) == 0 else 1)


if __name__ == "__main__":
    main()
