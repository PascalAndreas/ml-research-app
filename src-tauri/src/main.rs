#![cfg_attr(
    all(not(debug_assertions), target_os = "windows"),
    windows_subsystem = "windows"
)]

use tauri::Manager;

#[tauri::command]
async fn select_folder() -> Result<String, String> {
    tauri::api::dialog::blocking::FileDialogBuilder::default()
        .pick_folder()
        .ok_or("Folder not chosen".to_string())
        .map(|p| p.to_string_lossy().into())
}

fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![select_folder])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
