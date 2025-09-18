use clap::Parser;
use serde_json::json;
use reacher_core::{check_email, CheckEmailInput};
use tokio::runtime::Runtime;
use std::io::Write;
use std::env;

#[derive(Parser, Debug)]
#[clap(author, version, about, long_about = None)]
struct Args {
    #[clap(long)]
    to_email: Option<String>,
    #[clap(long)]
    json: bool,
}

fn main() {
    // You can set up a basic logger for debugging if needed
    env_logger::Builder::from_env(env_logger::Env::default().default_filter_or("info"))
        .format(|buf, record| {
            writeln!(buf, "{}: {}", record.level(), record.args())
        })
        .init();

    let args = Args::parse();
    let to_email = match args.to_email {
        Some(email) => email,
        None => {
            // If no email is provided, you can handle it or exit
            println!("No email provided.");
            return;
        }
    };

    let rt = Runtime::new().unwrap();
    let result = rt.block_on(async {
        let input = CheckEmailInput::new(vec![to_email.into()]);
        check_email(&input).await
    });

    if args.json {
        println!("{}", json!(result).to_string());
    } else {
        println!("{:?}", result);
    }
}