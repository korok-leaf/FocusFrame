//
//  Conditions.swift
//  FocusFrame
//
//  Created by Alex Qin on 2025-01-16.
//

import SwiftUI;
import Cocoa;


func changeWallpaper(with imagePath: String) throws {
    let script = """
    tell application "System Events"
        if not (exists process "System Events") then
            launch
        end if
        set the desktop picture to POSIX file "\(imagePath)"
    end tell
    """
    
    if let appleScript = NSAppleScript(source: script) {
        var error: NSDictionary?
        appleScript.executeAndReturnError(&error)
        
        if let error = error {
            print("AppleScript error: \(error)")
        } else {
            print("Wallpaper changed successfully via AppleScript.")
        }
    }
}

struct Conditions: View {
    @State var runAtLogin = false
    
    var body: some View {
        VStack {
            Text("Focus Frame")
                .bold()
            
            Divider()
                .frame(width: 200)
            
            CheckLists(runAtLogin: $runAtLogin)
                .onChange(of: runAtLogin) { value in
                    if value {
                        let wpPath = "/Users/alexqin/Desktop/projects/FocusFrame/FocusFrame/components/backend/wallpapers/wp1.png"
                        do {
                            try changeWallpaper(with: wpPath)
                        } catch {
                            print("Failed to change wallpaper: \(error)")
                        }
                    } else {
                        print("lol")
                    }
                }
                .padding()
            
        }
        .padding()
    }
}

struct CheckLists: View {
    @Binding var runAtLogin: Bool
    var body: some View {
        VStack(alignment: .leading) {
            Toggle(isOn: $runAtLogin) {
                Text("start at login")
            }
            Toggle(isOn: $runAtLogin) {
                Text("Show in menue")
            }
        }
    }
}

#Preview {
    Conditions();
}

