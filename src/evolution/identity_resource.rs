use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct IdentityResource {
    pub npub: String,
    pub desci_profile: Option<DeSciProfile>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DeSciProfile {
    pub nodes: Vec<NodeReference>,           // Research Objects publicados
    pub peer_reviews: Vec<PeerReview>,
    pub funding_contributions: Vec<FundingContribution>,
    pub reputation_score: DeSciReputation,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct NodeReference {
    pub dpid: String,                        // dPID do Node
    pub title: String,
    pub version: String,                     // versão atual
    pub published_at: u64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PeerReview {
    pub dpid: String,
    pub review_text: String,
    pub score: u8,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct FundingContribution {
    pub amount: f64,
    pub currency: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DeSciReputation {
    pub publication_count: u32,
    pub review_count: u32,
    pub citation_count: u32,
    pub overall_score: f32,                  // 0-100
}

impl IdentityResource {
    pub fn ensure_desci_profile(&mut self) {
        if self.desci_profile.is_none() {
            self.desci_profile = Some(DeSciProfile {
                nodes: Vec::new(),
                peer_reviews: Vec::new(),
                funding_contributions: Vec::new(),
                reputation_score: DeSciReputation {
                    publication_count: 0,
                    review_count: 0,
                    citation_count: 0,
                    overall_score: 0.0,
                },
            });
        }
    }

    pub fn add_desci_contribution(&mut self, node_ref: NodeReference, _role: &str) {
        self.ensure_desci_profile();
        if let Some(profile) = &mut self.desci_profile {
            profile.nodes.push(node_ref);
            profile.reputation_score.publication_count += 1;
            // Atualiza score combinado de confiança
        }
    }

    pub fn add_peer_review(&mut self, review: PeerReview) {
        self.ensure_desci_profile();
        if let Some(profile) = &mut self.desci_profile {
            profile.peer_reviews.push(review);
            profile.reputation_score.review_count += 1;
        }
    }
}
