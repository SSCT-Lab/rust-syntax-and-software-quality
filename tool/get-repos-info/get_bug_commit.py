


repo_path = "./results/checklists"
repo_list = [
  "actix/actix-web",
  "alacritty/alacritty",
  "denoland/deno",
  "benfred/py-spy",
  "bevyengine/bevy",
  "clap-rs/clap",
  "diem/diem",
  "dandavison/delta",
  "denisidoro/navi",
  "emilk/egui",
  "fdehau/tui-rs",
  "lapce/lapce",
  "neovide/neovide",
  "nushell/nushell",
  "ogham/exa",
  "rome/tools",
  "RustPython/RustPython",
  "servo/servo",
  "sharkdp/bat",
  "tikv/tikv",
  "tree-sitter/tree-sitter",
  "uutils/coreutils",
  "tock/tock",
  "wez/wezterm",
  "wasmerio/wasmer",
  "vectordotdev/vector",
  "tokio-rs/tokio",
  "tauri-apps/tauri",
  "starship/starship",
  "iced-rs/iced"
]

# 读取文件内容
with open(repo_path + repo_list[0], 'r') as file:
    lines = file.readlines()

# 提取每行数据的第二个值
second_values = [line.split()[1] for line in lines]

# 统计不同值的数量
unique_second_values = set(second_values)
count_unique_values = len(unique_second_values)

print(f"不同的第二个值的数量：{count_unique_values}")