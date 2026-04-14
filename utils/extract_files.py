import sys
import tarfile

# Function to extract specific files from a tar archive
def extract_files_from_tar(tar_filename, text_filename):
    try:
        # Open the tar archive for reading
        with tarfile.open(tar_filename, 'r') as tar:
            # Read the list of file names from the text file
            with open(text_filename, 'r') as text_file:
                file_names = set(line.strip() for line in text_file)

            # Iterate through the members in the tar archive
            for member in tar.getmembers():
                # Check if the member's name is in the list of file names
                print("Checking if " + member.name + " is in tar archive.")
                
                if member.name in file_names:
                    # Extract the member to the current directory
                    tar.extract(member)

        print("Extraction complete.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Check if the correct number of command-line arguments are provided
if len(sys.argv) != 3:
    print("Usage: python extract_files.py <tar_archive> <text_file>")
    sys.exit(1)

# Get the command-line arguments
tar_archive = sys.argv[1]
text_file = sys.argv[2]

# Call the function to extract files
extract_files_from_tar(tar_archive, text_file)
