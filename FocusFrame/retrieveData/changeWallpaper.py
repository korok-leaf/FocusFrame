import subprocess
import os

def test_applescript():
    applescript = '''
    display dialog "Hello from AppleScript!"
    '''
    
    try:
        result = subprocess.run(
            ["osascript", "-e", applescript],
            check=True,
            capture_output=True,
            text=True
        )
        print(f"AppleScript stdout: {result.stdout}")
        print(f"AppleScript stderr: {result.stderr}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to run AppleScript: {e}")
        print(f"AppleScript stderr: {e.stderr}")

def change_wallpaper_mac(image_path):
    # Ensure the path is in POSIX format
    image_path = os.path.abspath(image_path)
    
    # Create the AppleScript command
    applescript = f"""
    tell application "Finder"
        set desktop picture to POSIX file "{image_path}"
    end tell
    """
    
    try:
        # Run the AppleScript command via osascript and capture output
        result = subprocess.run(["osascript", "-e", applescript], check=True, capture_output=True, text=True)
        print("Wallpaper changed successfully on macOS!")
        print(result.stdout)  # Show output from AppleScript
    except subprocess.CalledProcessError as e:
        print(f"Failed to change wallpaper: {e}")
        print(e.output)  # Show output from AppleScript on error
        print(e.stderr)

if __name__ == "__main__":


    # THIS ONLY WORKS FOR TERMINAL, NOT VS CODE

    image_path = "/Users/alexqin/Desktop/projects/FocusFrame/FocusFrame/components/backend/wallpapers/wp1.png"  
    change_wallpaper_mac(image_path)
    #test_applescript()
