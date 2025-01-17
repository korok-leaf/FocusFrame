//
//  Conditions.swift
//  FocusFrame
//
//  Created by Alex Qin on 2025-01-16.
//

import SwiftUI;

struct Conditions: View {
    @State var runAtLogin = false
    
    var body: some View {
        VStack {
            Text("Focus Frame")
                .bold()
            
            Divider()
                .frame(width: 200)
            
            CheckLists(runAtLogin: $runAtLogin)
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

