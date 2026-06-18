use std::collections::HashMap;

// Types mock to compile snippet standalone if needed
#[derive(Debug, Clone)]
pub enum SkillType {
    ModelInvoked,
}

#[derive(Debug, Clone)]
pub struct SkillStep {
    pub order: u32,
    pub description: String,
    pub expected_output: String,
    pub validation: Option<String>,
}

#[derive(Debug, Clone)]
pub struct Skill {
    pub name: String,
    pub description: String,
    pub skill_type: SkillType,
    pub version: String,
    pub author: Option<String>,
    pub tags: Vec<String>,
    pub triggers: Vec<String>,
    pub steps: Vec<SkillStep>,
    pub examples: Vec<String>,
    pub dependencies: Vec<String>,
    pub metadata: HashMap<String, String>,
    pub okf_bundle_id: Option<String>,
}

pub fn desci_publish_skill() -> Skill {
    Skill {
        name: "desci-publish".to_string(),
        description: "Publica um Research Object no Open State Repository (DeSci)".to_string(),
        skill_type: SkillType::ModelInvoked,
        version: "1.0.0".to_string(),
        author: Some("Cathedral ARKHE".to_string()),
        tags: vec!["desci".to_string(), "publish".to_string(), "research".to_string()],
        triggers: vec!["publicar pesquisa".to_string(), "desci publish".to_string()],
        steps: vec![
            SkillStep {
                order: 1,
                description: "Recebe Research Object em formato OKF Bundle".to_string(),
                expected_output: "Conteúdo validado".to_string(),
                validation: Some("Formato OKF válido".to_string()),
            },
            SkillStep {
                order: 2,
                description: "Registra no Open State Repository e gera dPID".to_string(),
                expected_output: "dPID gerado".to_string(),
                validation: None,
            },
            SkillStep {
                order: 3,
                description: "Armazena no HashTree como OKF Bundle com referência ao dPID".to_string(),
                expected_output: "ContentHash".to_string(),
                validation: None,
            },
        ],
        examples: vec!["Publicar research object sobre IA soberana".to_string()],
        dependencies: vec!["desci-api".to_string()],
        metadata: {
            let mut m = HashMap::new();
            m.insert("platform".to_string(), "desci".to_string());
            m
        },
        okf_bundle_id: None,
    }
}
