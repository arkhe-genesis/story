use clap::Subcommand;
use arkhe::integrations::desci_client::DesciClient;
use arkhe::evolution::desci_node_resource::DeSciNodeResource;
use arkhe::evolution::sepl_desci::AutogenesisOperator;
use arkhe::evolution::identity_resource::{IdentityResource, NodeReference, PeerReview};

#[derive(Subcommand)]
pub enum DesciCommands {
    Publish {
        #[arg(short, long)] title: String,
        #[arg(short, long)] orcid: Option<String>,
        #[arg(long)] dpid: Option<String>,
    },
    Evolve {
        #[arg(short, long)] node_id: String,
        #[arg(short, long)] target_metric: String,
    },
    Profile,
}

impl DesciCommands {
    pub async fn execute(&self) -> Result<(), Box<dyn std::error::Error>> {
        let client = DesciClient::new(None);
        match self {
            DesciCommands::Publish { title, orcid, dpid } => {
                let node = DeSciNodeResource::new(title, dpid.as_deref().unwrap_or("dpid-temp"), "npub123", orcid.as_deref());
                let generated_dpid = client.register_node(title, "hash_dummy").await?;

                println!("✅ Research Object publicado");
                if let Some(dpid_val) = dpid {
                    println!("   dPID: {}", dpid_val);
                } else {
                    println!("   dPID: {}", generated_dpid);
                }
                println!("   CID: bafkre...");
                println!("   HashTree: QmXyz...");
                Ok(())
            }
            DesciCommands::Evolve { node_id, target_metric } => {
                let mut node = DeSciNodeResource::new("Dummy Title", "dpid-temp", "npub123", None);
                node.node_id = node_id.clone();
                let operator = AutogenesisOperator { npub: "npub123".to_string() };

                println!("🔍 [SEPL] Refletindo sobre Node...");
                let proposal = operator.propose_desci_improvement(&node, target_metric).await?;
                println!("💡 [SEPL] Proposta: {}", proposal.rationale);

                let verification = operator.verify_desci_node(&node).await?;
                if verification.success {
                    println!("🧪 [SEPL] Verificação aprovada");
                    operator.commit_desci_version(&proposal, &verification, &mut node).await?;
                    println!("✅ [SEPL] Commitado ({} → {})", node.versions[0].version, node.current_version);
                } else {
                    println!("❌ [SEPL] Verificação falhou");
                }
                Ok(())
            }
            DesciCommands::Profile => {
                let mut identity = IdentityResource {
                    npub: "npub123".to_string(),
                    desci_profile: None,
                };
                identity.add_desci_contribution(NodeReference {
                    dpid: "46".to_string(),
                    title: "Test".to_string(),
                    version: "1.0.0".to_string(),
                    published_at: chrono::Utc::now().timestamp() as u64,
                }, "author");
                identity.add_peer_review(PeerReview {
                    dpid: "46".to_string(),
                    review_text: "Good".to_string(),
                    score: 8,
                });

                if let Some(profile) = identity.desci_profile {
                    println!("🧑‍🔬 Perfil DeSci");
                    println!("   Publicações: {}", profile.reputation_score.publication_count);
                    println!("   Revisões: {}", profile.reputation_score.review_count);
                    println!("   Reputação: {}/100", profile.reputation_score.overall_score);
                }
                Ok(())
            }
        }
    }
}
