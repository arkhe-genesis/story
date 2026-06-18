// src/evolution/desci_node_resource.rs
//! DeSciNodeResource — Research Objects versionáveis integrados ao HashTree + Open State Repository

use serde::{Serialize, Deserialize};
use std::collections::HashMap;
use chrono::Utc;

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub enum ResearchComponentType {
    Manuscript,
    Dataset,
    Code,
    Model,
    Pipeline,
    Supplementary,
    Custom(String),
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ResearchComponent {
    pub component_type: ResearchComponentType,
    pub name: String,
    pub hash: String,                    // Hash no HashTree
    pub cid: Option<String>,             // IPFS CID (interoperabilidade)
    pub size_bytes: Option<u64>,
    pub metadata: HashMap<String, String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ContributorCredit {
    pub npub: String,
    pub orcid: Option<String>,
    pub role: String,                    // "author", "data-curator", "reviewer", "maintainer"
    pub contribution_score: f64,         // 0.0 - 1.0
    pub contribution_description: Option<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct NodeVersion {
    pub version: String,
    pub hash: String,
    pub created_at: u64,
    pub created_by: String,
    pub changelog: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DeSciNodeResource {
    pub node_id: String,                 // ID interno do DeSci
    pub dpid: String,                    // Decentralized Persistent Identifier
    pub title: String,
    pub abstract_text: Option<String>,
    pub components: Vec<ResearchComponent>,
    pub contributors: Vec<ContributorCredit>,
    pub orcid_links: Vec<String>,
    pub versions: Vec<NodeVersion>,
    pub current_version: String,
    pub license: Option<String>,
    pub keywords: Vec<String>,
}

impl DeSciNodeResource {
    pub fn new(
        title: &str,
        dpid: &str,
        author_npub: &str,
        author_orcid: Option<&str>,
    ) -> Self {
        let now = Utc::now().timestamp() as u64;
        let node_id = format!("desci:{}", uuid::Uuid::new_v4());

        let contributors = vec![ContributorCredit {
            npub: author_npub.to_string(),
            orcid: author_orcid.map(|s| s.to_string()),
            role: "author".to_string(),
            contribution_score: 1.0,
            contribution_description: Some("Initial creation".to_string()),
        }];

        Self {
            node_id,
            dpid: dpid.to_string(),
            title: title.to_string(),
            abstract_text: None,
            components: Vec::new(),
            contributors,
            orcid_links: author_orcid.map(|o| vec![o.to_string()]).unwrap_or_default(),
            versions: vec![NodeVersion {
                version: "v1".to_string(),
                hash: "".to_string(),
                created_at: now,
                created_by: author_npub.to_string(),
                changelog: "Initial version".to_string(),
            }],
            current_version: "v1".to_string(),
            license: Some("CC-BY-4.0".to_string()),
            keywords: vec![],
        }
    }

    pub fn add_component(&mut self, component: ResearchComponent) {
        self.components.push(component);
    }

    pub fn add_contributor(&mut self, contributor: ContributorCredit) {
        self.contributors.push(contributor);
    }

    pub fn create_new_version(&mut self, changelog: &str, author: &str) -> String {
        let new_version = format!("v{}", self.versions.len() + 1);
        let now = Utc::now().timestamp() as u64;

        self.versions.push(NodeVersion {
            version: new_version.clone(),
            hash: "".to_string(), // será preenchido após commit no HashTree
            created_at: now,
            created_by: author.to_string(),
            changelog: changelog.to_string(),
        });

        self.current_version = new_version.clone();
        new_version
    }
}
