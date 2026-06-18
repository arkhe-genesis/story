use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DesciNodeMetadata {
    pub dpid: String,
    pub title: String,
    pub manifest_cid: String,
    pub version: String,
}

pub struct DesciClient {
    client: reqwest::Client,
    pub api_key: Option<String>,
}

impl DesciClient {
    pub fn new(api_key: Option<String>) -> Self {
        Self {
            client: reqwest::Client::new(),
            api_key,
        }
    }

    /// Registra um Node no Open State Repository e retorna o dPID
    pub async fn register_node(&self, title: &str, content_hash: &str) -> Result<String, Box<dyn std::error::Error>> {
        let payload = serde_json::json!({
            "title": title,
            "content_hash": content_hash,
            "metadata": {
                "description": "ARKHE Research Object",
            }
        });

        // Simula request em API fake
        // url: https://api.desci.com/v1/nodes/register
        let res = self.client.post("https://httpbin.org/post")
            .json(&payload)
            .send()
            .await?;

        let _ = res.text().await?;

        // Simulação do dPID retornado
        let dpid = format!("dpid-{}-arkhe", chrono::Utc::now().timestamp() % 100000);
        println!("📡 [DeSci API] Registrando Node '{}' (hash: {}) -> {}", title, content_hash, dpid);
        Ok(dpid)
    }

    /// Resolve um dPID para obter metadados do Research Object
    pub async fn resolve_dpid(&self, dpid: &str) -> Result<DesciNodeMetadata, Box<dyn std::error::Error>> {
        // url: https://api.desci.com/v1/nodes/resolve/{dpid}
        let res = self.client.get("https://httpbin.org/get")
            .query(&[("dpid", dpid)])
            .send()
            .await?;

        let _ = res.text().await?;

        println!("📡 [DeSci API] Resolvendo dPID: {}", dpid);
        Ok(DesciNodeMetadata {
            dpid: dpid.to_string(),
            title: "Simulated Research Object".to_string(),
            manifest_cid: format!("Qm{}", chrono::Utc::now().timestamp()),
            version: "1.0.0".to_string(),
        })
    }
}
