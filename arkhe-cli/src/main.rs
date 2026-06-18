mod commands;

use clap::Parser;
use commands::desci::{DesciCommands};
use commands::octra::{OctraCommands};

#[derive(Parser)]
#[command(name = "arkhe-cli")]
pub struct Cli {
    #[command(subcommand)]
    pub command: AppCommands,
}

#[derive(clap::Subcommand)]
pub enum AppCommands {
    #[command(subcommand)]
    Desci(DesciCommands),
    #[command(subcommand)]
    Octra(OctraCommands),
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let cli = Cli::parse();
    match &cli.command {
        AppCommands::Desci(cmd) => cmd.execute().await,
        AppCommands::Octra(cmd) => cmd.execute().await,
    }
}
