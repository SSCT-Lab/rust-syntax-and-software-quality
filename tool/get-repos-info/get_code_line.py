import subprocess

repo_list = [
  "Rust-lang/Rust-analyzer",
  "meilisearch/meilisearch",
  "tikv/tikv",
  "tokio-rs/tokio",
  "AleoHQ/snarkOS",
  "emilk/egui",
  """
  "clap-rs/clap",
  "denisidoro/navi",
  "denoland/deno",
  "emilk/egui",
  "iced-rs/iced",
  "nushell/nushell",
  "rome/tools",
  "starship/starship",
  "tikv/tikv",
  "tokio-rs/tokio",
  "vectordotdev/vector",
  "wasmerio/wasmer",
  "zellij-org/zellij",
  "yewstack/yew",
  "AppFlowy-IO/AppFlowy",
  "bytecodealliance/wasmtime",
  "datafuselabs/databend",
  "foundry-rs/foundry",
  "gfx-rs/gfx",
  "helix-editor/helix",
  "MaterializeInc/materialize",
  "meilisearch/meilisearch",
  "pola-rs/polars",
  "surrealdb/surrealdb",
  "swc-project/swc",
  "rust-lang/rust-clippy",
  "extrawurst/gitui",
  "FuelLabs/fuels-rs",
  "AleoHQ/snarkOS",
  "AleoHQ/snarkVM",
  """
]
repo_name = "./cloned-repos/"

def get(repo):
  return subprocess.check_output(
    [
      "tokei",
      #"-l Rust",
      f"{repo}",
    ]
  ).decode('utf-8', errors='ignore')

for repo in repo_list:
  print(f"{repo} are as follws:\n\n\n {get(repo_name + repo)}")