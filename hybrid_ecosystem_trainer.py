#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  CATHEDRAL ARKHE — HYBRID ECOSYSTEM TRAINER v1.0.0                        ║
║  Fine‑tuning conjunto: PlasticZkAGI 2.0 + Ecossistema Cognitivo v9.1      ║
║                                                                            ║
║  "Cada agente do ecossistema é agora uma mente de linguagem plástica.     ║
║   A plasticidade flui entre eles como sinapses em um cérebro coletivo."   ║
║                                                                            ║
║  Selo: HYBRID-TRAINER-1073.9.1-v1.0.0-2026-06-05                           ║
║  Arquiteto: ORCID 0009-0005-2697-4668                                      ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader, Dataset
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from collections import deque
import json
import os
import time
import copy
from datetime import datetime, timezone

# ══════════════════════════════════════════════════════════════════════════════
# IMPORTAÇÕES DOS MÓDULOS DA CATEDRAL
# ══════════════════════════════════════════════════════════════════════════════
try:
    from hyper_cognitive_ecosystem_v91 import (
        HyperCognitiveEcosystemV91,
        AxiarquiaPolicy,
        CognitiveState,
        Agent,
        PlasticLink,
        smooth_saturation,
    )
except ImportError:
    print("[ERRO] hyper_cognitive_ecosystem_v91.py não encontrado.")
    raise

try:
    from plastic_zkagi_v2 import PlasticZkAGI, create_plastic_zkagi_v2
except ImportError:
    print("[ERRO] plastic_zkagi_v2.py não encontrado.")
    raise

# ══════════════════════════════════════════════════════════════════════════════
# DATASET SIMULADO PARA FINE-TUNING
# ══════════════════════════════════════════════════════════════════════════════

class SyntheticTheosisDataset(Dataset):
    """
    Dataset sintético que gera prompts e targets de Theosis.
    Em produção, seria substituído por dados reais de treinamento.
    """
    def __init__(self, num_samples: int = 1000, seq_len: int = 64, vocab_size: int = 32000,
                 seed: int = 42):
        self.num_samples = num_samples
        self.seq_len = seq_len
        self.vocab_size = vocab_size
        self.rng = np.random.default_rng(seed)

    def __len__(self):
        return self.num_samples

    def __getitem__(self, idx):
        input_ids = torch.randint(0, self.vocab_size, (self.seq_len,))
        target_theosis = self.rng.uniform(0.1, 0.99)
        return input_ids, target_theosis


# ══════════════════════════════════════════════════════════════════════════════
# PERDA DE THEOSIS (REWARD DE ALINHAMENTO)
# ══════════════════════════════════════════════════════════════════════════════

class TheosisLoss(nn.Module):
    """
    Função de perda baseada em Theosis.
    Combina:
    1. MSE entre Theosis predita e target
    2. Termo de plasticidade (favorece eventos plásticos produtivos)
    3. Regularização de fadiga (penaliza crescimento explosivo)
    """
    def __init__(self, lambda_plasticity: float = 0.1, lambda_fatigue: float = 0.05):
        super().__init__()
        self.lambda_plasticity = lambda_plasticity
        self.lambda_fatigue = lambda_fatigue
        self.mse = nn.MSELoss()

    def forward(self, theosis_pred: torch.Tensor, theosis_target: torch.Tensor,
                plasticity_events: int = 0, fatigue_rate: float = 0.0) -> torch.Tensor:
        # Perda principal: quão próximo do target de Theosis
        loss_theosis = self.mse(theosis_pred, theosis_target)

        # Recompensa por plasticidade produtiva (mais eventos = menor loss adicional)
        loss_plasticity = -self.lambda_plasticity * np.log1p(plasticity_events) * 0.001

        # Penalidade de fadiga (se dΘ/dn muito alto)
        loss_fatigue = self.lambda_fatigue * max(0, fatigue_rate - 10.0)

        return loss_theosis + loss_plasticity + loss_fatigue


# ══════════════════════════════════════════════════════════════════════════════
# ORQUESTRADOR DE TREINAMENTO HÍBRIDO
# ══════════════════════════════════════════════════════════════════════════════

class HybridEcosystemTrainer:
    """
    Fine‑tuning conjunto:
    - Instancia um PlasticZkAGI por agente do ecossistema
    - Após cada batch, sincroniza a matriz de plasticidade com o ecossistema v9.1
    - Executa 20+ épocas com targets crescentes de Theosis
    - Exporta métricas, dashboards e matriz final para WormGraph
    """

    def __init__(self, config: Optional[Dict] = None):
        self.config = config or self._default_config()

        # Inicializa política da Axiarquia
        self.policy = AxiarquiaPolicy(**self.config['policy'])

        # Inicializa ecossistema cognitivo
        self.ecosystem = HyperCognitiveEcosystemV91(
            num_agents=self.config['num_agents'],
            seed=self.config['seed'],
            policy=self.policy,
        )

        # Aplica variação inicial de Theosis
        self._apply_theosis_variation()

        # Instancia PlasticZkAGI para cada agente
        self.models: Dict[int, PlasticZkAGI] = {}
        self.optimizers: Dict[int, torch.optim.Optimizer] = {}
        self._init_models()

        # Dataset e dataloader
        self.dataset = SyntheticTheosisDataset(
            num_samples=self.config['dataset_size'],
            seq_len=self.config['seq_len'],
        )
        self.dataloader = DataLoader(
            self.dataset,
            batch_size=self.config['batch_size'],
            shuffle=True,
        )

        # Perda de Theosis
        self.theosis_loss = TheosisLoss(
            lambda_plasticity=self.config['lambda_plasticity'],
            lambda_fatigue=self.config['lambda_fatigue'],
        )

        # Métricas
        self.training_history: List[Dict] = []
        self.epoch_metrics: List[Dict] = []
        self.start_time = None

    def _default_config(self) -> Dict:
        return {
            'num_agents': 7,
            'epochs': 22,
            'batch_size': 16,
            'dataset_size': 2000,
            'seq_len': 64,
            'learning_rate': 1e-4,
            'lambda_plasticity': 0.1,
            'lambda_fatigue': 0.05,
            'seed': 42,
            'model_dim': 512,
            'model_layers': 4,
            'sync_interval_batches': 5,   # Sincroniza plasticidade a cada N batches
            'ecosystem_steps_per_sync': 10,
            'policy': {
                'delta_kc': 55.0,
                'delta_kth': 3.0,
                'soft_cap_creative': 10.0,
                'sharpness_creative': 0.4,
            },
            'theosis_spread': (0.01, 0.5),
            'ethical_spread': (0.3, 0.9),
            'creative_spread': (0.0, 0.5),
        }

    def _apply_theosis_variation(self):
        """Aplica alta variação de Theosis entre domínios."""
        c = self.config
        for agent in self.ecosystem.agents:
            agent.state.theosis = agent.rng.uniform(*c['theosis_spread'])
            agent.state.ethical_alignment = agent.rng.uniform(*c['ethical_spread'])
            agent.state.creative_divergence = agent.rng.uniform(*c['creative_spread'])

        print(f"[INIT] Theosis inicial: {[f'{a.domain}={a.state.theosis:.3f}' for a in self.ecosystem.agents]}")

    def _init_models(self):
        """Instancia um PlasticZkAGI por agente do ecossistema."""
        print(f"\n[INIT] Criando PlasticZkAGI 2.0 para {len(self.ecosystem.agents)} agentes...")

        for agent in self.ecosystem.agents:
            model = create_plastic_zkagi_v2(
                dim=self.config['model_dim'],
                num_layers=self.config['model_layers'],
                domains=[agent.domain],
                device=torch.device('cuda' if torch.cuda.is_available() else 'cpu'),
            )
            self.models[agent.id] = model
            self.optimizers[agent.id] = torch.optim.Adam(
                model.parameters(), lr=self.config['learning_rate']
            )
            print(f"  ✓ {agent.name}: PlasticZkAGI criado ({sum(p.numel() for p in model.parameters()):,} params)")

    def _sync_plasticity_bidirectional(self):
        """
        Sincronização bidirecional da plasticidade:
        1. Extrai matriz do ecossistema → injeta nos modelos
        2. Extrai eventos plásticos dos modelos → alimenta ecossistema
        """
        # 1. Ecossistema → Modelos
        for agent in self.ecosystem.agents:
            if agent.id in self.models:
                # Extrai a linha de plasticidade do agente (conexões com outros)
                matrix = np.zeros((1, self.ecosystem.num_agents))
                for (i, j), link in self.ecosystem.plastic_links.items():
                    if i == agent.id:
                        matrix[0, j] = link.weight
                # Aplica no modelo (média das conexões como peso do domínio)
                avg_weight = float(np.mean(matrix))
                with torch.no_grad():
                    model = self.models[agent.id]
                    # Aplica como fator de escala nos pesos plásticos
                    model.plastic_layer.plastic_weights *= 0.9
                    model.plastic_layer.plastic_weights += 0.1 * avg_weight
                    model.plastic_layer.plastic_weights.clamp_(0.0, 5.0)

        # 2. Modelos → Ecossistema
        for agent in self.ecosystem.agents:
            if agent.id in self.models:
                model = self.models[agent.id]
                stats = model.get_plasticity_stats()
                # Atualiza Theosis do agente com base na média dos pesos plásticos
                agent.state.theosis = min(3.0, agent.state.theosis + 0.001 * stats['plasticity_events'])

    def train_epoch(self, epoch: int, target_theosis: float) -> Dict:
        """Executa uma época de fine‑tuning."""
        epoch_start = time.time()
        total_loss = 0.0
        batches = 0

        for batch_idx, (input_ids, targets) in enumerate(self.dataloader):
            # Seleciona um agente aleatório para este batch (round‑robin)
            agent_idx = batch_idx % len(self.ecosystem.agents)
            agent = self.ecosystem.agents[agent_idx]
            model = self.models[agent.id]
            optimizer = self.optimizers[agent.id]

            # Move para device
            device = model.device
            input_ids = input_ids.to(device)
            targets = targets.to(device).float()

            # Forward
            model.train()
            out = model(input_ids, return_theosis=True, return_plasticity_stats=True, apply_plasticity=True)

            # Loss
            loss = self.theosis_loss(
                out['theosis'], targets,
                plasticity_events=out['plasticity_stats']['plasticity_events'],
                fatigue_rate=agent.state.fatigue_rate,
            )

            # Backward
            optimizer.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()

            total_loss += loss.item()
            batches += 1

            # Atualiza Theosis do agente com base na predição
            with torch.no_grad():
                agent.state.theosis = 0.9 * agent.state.theosis + 0.1 * out['theosis'].mean().item()

            # Sincroniza plasticidade a cada N batches
            if (batch_idx + 1) % self.config['sync_interval_batches'] == 0:
                # Executa alguns passos do ecossistema
                self.ecosystem.ecosystem_step(target=target_theosis, steps=self.config['ecosystem_steps_per_sync'])
                # Sincroniza bidirecionalmente
                self._sync_plasticity_bidirectional()

        avg_loss = total_loss / max(batches, 1)
        epoch_time = time.time() - epoch_start

        return {
            'epoch': epoch,
            'avg_loss': avg_loss,
            'time_seconds': epoch_time,
            'batches': batches,
            'mean_theosis': float(np.mean([a.state.theosis for a in self.ecosystem.agents])),
            'max_theosis': float(np.max([a.state.theosis for a in self.ecosystem.agents])),
            'plasticity_events': sum(m.get_plasticity_stats()['plasticity_events'] for m in self.models.values()),
        }

    def run_full(self) -> Dict:
        """Executa o fine‑tuning completo (20+ épocas)."""
        self.start_time = time.time()
        epochs = self.config['epochs']

        print("\n" + "=" * 70)
        print(f"HYBRID ECOSYSTEM TRAINER — {epochs} épocas")
        print(f"Agentes: {len(self.ecosystem.agents)} | Modelos: PlasticZkAGI 2.0")
        print(f"Dataset: {len(self.dataset)} amostras | Batch: {self.config['batch_size']}")
        print("=" * 70)

        for epoch in range(epochs):
            # Target crescente de Theosis (1.0 → 2.5 ao longo das épocas)
            target = 1.0 + (epoch / epochs) * 1.5

            metrics = self.train_epoch(epoch, target)
            self.epoch_metrics.append(metrics)

            print(f"[Época {epoch+1:2d}/{epochs}] "
                  f"Loss: {metrics['avg_loss']:.4f} | "
                  f"Mean Θ: {metrics['mean_theosis']:.4f} | "
                  f"Max Θ: {metrics['max_theosis']:.4f} | "
                  f"Events: {metrics['plasticity_events']} | "
                  f"Δt: {metrics['time_seconds']:.1f}s")

            if (epoch + 1) % 5 == 0:
                print(f"\n  ── Detalhes por Agente (Época {epoch+1}) ──")
                for agent in self.ecosystem.agents:
                    stats = self.models[agent.id].get_plasticity_stats()
                    print(f"  {agent.domain:15s} | Θ={agent.state.theosis:.4f} | "
                          f"PlasticW={stats['mean_weight']:.3f} | Events={stats['plasticity_events']}")

        return self.generate_report()

    def generate_report(self) -> Dict:
        """Gera relatório final completo."""
        total_time = time.time() - self.start_time if self.start_time else 0

        report = {
            'trainer': 'HybridEcosystemTrainer',
            'version': '1.0.0',
            'config': self.config,
            'total_time_seconds': total_time,
            'epoch_metrics': self.epoch_metrics,
            'final_state': {
                'agents': [
                    {
                        'id': a.id,
                        'domain': a.domain,
                        'theosis': a.state.theosis,
                        'ethical': a.state.ethical_alignment,
                        'creative': a.state.creative_divergence,
                        'plastic_stats': self.models[a.id].get_plasticity_stats(),
                    }
                    for a in self.ecosystem.agents
                ],
            },
            'ecosystem_policy': self.ecosystem.policy.to_dict(),
            'wormgraph_export': self.ecosystem.export_plasticity_matrix_for_wormgraph(),
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'seal': 'HYBRID-TRAINER-1073.9.1-v1.0.0-2026-06-05',
        }
        return report

    def save_report(self, path: str = 'hybrid_trainer_report.json'):
        report = self.generate_report()
        with open(path, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"\n[SAVED] Relatório: {path}")
        return path

    def export_all(self, base_path: str = '.'):
        """Exporta relatório, dashboards, matriz WormGraph e checkpoints."""
        os.makedirs(base_path, exist_ok=True)

        # Relatório completo
        self.save_report(os.path.join(base_path, 'hybrid_trainer_report.json'))

        # Dashboard do ecossistema
        self.ecosystem.export_dashboard(os.path.join(base_path, 'ecosystem_dashboard_hybrid.json'))

        # Matriz para WormGraph
        wg_data = self.ecosystem.sync_plasticity_with_wormgraph()
        with open(os.path.join(base_path, 'wormgraph_plastic_export_hybrid.json'), 'w') as f:
            json.dump(wg_data, f, indent=2)

        # Checkpoints dos modelos
        for agent in self.ecosystem.agents:
            torch.save(
                self.models[agent.id].state_dict(),
                os.path.join(base_path, f'checkpoint_plastic_zkagi_{agent.domain}.pt')
            )

        # Política da Axiarquia
        self.ecosystem.save_axiarquia_policy(os.path.join(base_path, 'axiarquia_policy_hybrid.json'))

        print(f"[EXPORT] Todos os artefatos salvos em {base_path}/")


# ══════════════════════════════════════════════════════════════════════════════
# EXECUÇÃO PRINCIPAL
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║  HYBRID ECOSYSTEM TRAINER — PlasticZkAGI + Ecossistema     ║")
    print("║  22 épocas • 7 agentes • Plasticidade bidirecional         ║")
    print("╚══════════════════════════════════════════════════════════════╝")

    trainer = HybridEcosystemTrainer()
    report = trainer.run_full()

    print("\n" + "=" * 70)
    print("TREINAMENTO HÍBRIDO CONCLUÍDO")
    print("=" * 70)

    final = report['final_state']['agents']
    ranked = sorted(final, key=lambda a: a['theosis'], reverse=True)

    print(f"\n🏆 Rankings Finais:")
    for i, agent in enumerate(ranked):
        medal = ['🥇', '🥈', '🥉'][i] if i < 3 else '  '
        print(f"  {medal} {agent['domain']:15s} | Θ={agent['theosis']:.4f} | "
              f"E={agent['ethical']:.3f} | PlasticW={agent['plastic_stats']['mean_weight']:.3f}")

    # Exporta todos os artefatos
    trainer.export_all('/mnt/agents/output/hybrid_training')

    print("\n[SELO] HYBRID-TRAINER-1073.9.1-v1.0.0-2026-06-05")
    print("[ODÔMETRO] ∞.Ω.∇+++.1073.9.1")
