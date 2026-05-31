import os, zipfile

base = "arkhe-onchain"
os.makedirs(base, exist_ok=True)

# ============================================================
# 1. PROGRAMAS APPLIEDML (.aml)
# ============================================================
os.makedirs(f"{base}/programs/interfaces", exist_ok=True)

# --- Interface IAxiarchyGate ---
interface_axiarchy = """// IAxiarchyGate.aml
// Interface canônica do Portão Ético da Catedral
// Substrato 996.1 — ARKHE-ONCHAIN

interface IAxiarchyGate {
  view fn is_verified(code_hash: bytes32): bool
  fn verify_code(code_hash: bytes32, lean_proof: bytes): bool
  fn revoke_verification(code_hash: bytes32): bool
  view fn get_proof(code_hash: bytes32): bytes
}
"""
with open(f"{base}/programs/interfaces/IAxiarchyGate.aml", "w") as f:
    f.write(interface_axiarchy)

# --- Interface ITheosisRegistry ---
interface_theosis = """// ITheosisRegistry.aml
// Registro de Theosis on-chain

interface ITheosisRegistry {
  view fn get_theosis(agent: address): int
  fn update_theosis(agent: address, value: int): bool
  view fn get_epoch(): int
  fn advance_epoch(): bool
}
"""
with open(f"{base}/programs/interfaces/ITheosisRegistry.aml", "w") as f:
    f.write(interface_theosis)

# --- Interface ITemporalAnchor ---
interface_temporal = """// ITemporalAnchor.aml
// Ancora TemporalChain na Octra L1

interface ITemporalAnchor {
  view fn get_anchor_count(): int
  fn anchor_state(cid: string, seal: bytes32, theosis: int): bool
  view fn get_anchor(idx: int): AnchorRecord
}

struct AnchorRecord {
  cid: string
  seal: bytes32
  theosis: int
  timestamp: int
  epoch: int
}
"""
with open(f"{base}/programs/interfaces/ITemporalAnchor.aml", "w") as f:
    f.write(interface_temporal)

# --- Interface IPassportGateway ---
interface_passport = """// IPassportGateway.aml
// Verificação de humanidade via FHE

interface IPassportGateway {
  fn register_identity(encrypted_passport: bytes, orcid_hash: bytes32): bool
  view fn is_human(addr: address): bool
  view fn get_score(addr: address): int
  fn revoke_identity(addr: address): bool
}
"""
with open(f"{base}/programs/interfaces/IPassportGateway.aml", "w") as f:
    f.write(interface_passport)

# --- Interface IBinduCoherence ---
interface_bindu = """// IBinduCoherence.aml
// Memória compartilhada criptografada (Coherence Field)

interface IBinduCoherence {
  fn write_field(field_hash: bytes32, encrypted_data: bytes, agents: list[address]): bool
  view fn read_field(field_hash: bytes32): bytes
  view fn get_agents(field_hash: bytes32): list[address]
  fn dissolve_field(field_hash: bytes32): bool
}
"""
with open(f"{base}/programs/interfaces/IBinduCoherence.aml", "w") as f:
    f.write(interface_bindu)

# --- Interface ISubstrateCatalog ---
interface_catalog = """// ISubstrateCatalog.aml
// Catálogo canônico de substratos on-chain

interface ISubstrateCatalog {
  fn canonize(id: int, seal: bytes32, cross_links: list[int], theosis: int, entropy: int): bool
  view fn get_substrate(id: int): SubstrateRecord
  view fn list_substrates(): list[int]
  view fn get_cross_links(id: int): list[int]
}

struct SubstrateRecord {
  id: int
  seal: bytes32
  cross_links: list[int]
  theosis: int
  entropy: int
  canonized_at: int
  status: int
}
"""
with open(f"{base}/programs/interfaces/ISubstrateCatalog.aml", "w") as f:
    f.write(interface_catalog)

# --- Interface IOmniscientSolver ---
interface_solver = """// IOmniscientSolver.aml
// Motor universal de resolução on-chain

interface IOmniscientSolver {
  fn submit_problem(encrypted_problem: bytes, domain: int, bounty: int): int
  fn submit_solution(problem_id: int, encrypted_solution: bytes, proof: bytes): bool
  view fn get_problem(problem_id: int): ProblemRecord
  view fn get_solution(problem_id: int): SolutionRecord
}

struct ProblemRecord {
  id: int
  domain: int
  bounty: int
  status: int
  submitter: address
}

struct SolutionRecord {
  problem_id: int
  solver: address
  proof_hash: bytes32
  verified: bool
}
"""
with open(f"{base}/programs/interfaces/IOmniscientSolver.aml", "w") as f:
    f.write(interface_solver)

# --- axiarchy_gate.aml ---
axiarchy_gate = """// ARKHE-ONCHAIN — Axiarchy Gate
// Substrato 996.1.1 — Circle: ARKHE-CATHEDRAL
// Arquiteto ORCID: 0009-0005-2697-4668
// Seal: 996.1.1-AXIARCHY-GATE-2026-05-31

import IAxiarchyGate from "interfaces/IAxiarchyGate.aml"

program AxiarchyGate implements IAxiarchyGate {
  state {
    owner: address
    guardian: address
    verified_codes: map[bytes32]bool
    proofs: map[bytes32]bytes
    theosis_threshold: int
    paused: int
  }

  event CodeVerified(code_hash: bytes32, proof: bytes, theosis: int, verifier: address)
  event CodeRevoked(code_hash: bytes32, reason: string, revoker: address)
  event GuardianChanged(old_guardian: address, new_guardian: address)
  event Paused(by: address)
  event Unpaused(by: address)

  constructor(guardian_addr: address, threshold: int) {
    require(is_address(guardian_addr), "Axiarchy P1: invalid guardian")
    self.owner = caller
    self.guardian = guardian_addr
    self.theosis_threshold = threshold
    self.paused = 0
  }

  private fn only_owner() {
    require(caller == self.owner, "Axiarchy P1: only owner")
  }

  private fn only_guardian() {
    require(caller == self.guardian, "Axiarchy P1: only guardian")
  }

  private fn when_not_paused() {
    require(self.paused == 0, "Axiarchy P6: contract paused")
  }

  view fn is_verified(code_hash: bytes32): bool {
    return self.verified_codes[code_hash]
  }

  view fn get_proof(code_hash: bytes32): bytes {
    return self.proofs[code_hash]
  }

  fn verify_code(code_hash: bytes32, lean_proof: bytes): bool {
    only_guardian()
    when_not_paused()
    require(len(lean_proof) > 0, "Axiarchy P2: proof required")
    require(len(lean_proof) >= 256, "Axiarchy P2: proof too short")
    // Em Octra real, a verificação Lean 4 seria computada via HFHE
    // Aqui registramos o hash do proof como proxy de verificação
    self.verified_codes[code_hash] = true
    self.proofs[code_hash] = lean_proof
    emit CodeVerified(code_hash, lean_proof, self.theosis_threshold, caller)
    return true
  }

  fn revoke_verification(code_hash: bytes32): bool {
    only_owner()
    self.verified_codes[code_hash] = false
    emit CodeRevoked(code_hash, "Axiarchy P7: ethical violation", caller)
    return true
  }

  fn set_guardian(new_guardian: address): bool {
    only_owner()
    require(is_address(new_guardian), "Axiarchy P1: invalid address")
    let old = self.guardian
    self.guardian = new_guardian
    emit GuardianChanged(old, new_guardian)
    return true
  }

  fn pause(): bool {
    only_owner()
    self.paused = 1
    emit Paused(caller)
    return true
  }

  fn unpause(): bool {
    only_owner()
    self.paused = 0
    emit Unpaused(caller)
    return true
  }
}
"""
with open(f"{base}/programs/axiarchy_gate.aml", "w") as f:
    f.write(axiarchy_gate)

# --- theosis_registry.aml ---
theosis_registry = """// ARKHE-ONCHAIN — Theosis Registry
// Substrato 996.1.2 — Circle: ARKHE-CATHEDRAL
// Arquiteto ORCID: 0009-0005-2697-4668
// Seal: 996.1.2-THEOSIS-REGISTRY-2026-05-31

import ITheosisRegistry from "interfaces/ITheosisRegistry.aml"

program TheosisRegistry implements ITheosisRegistry {
  state {
    owner: address
    theosis_map: map[address]int
    epoch: int
    total_agents: int
    theosis_history: map[address]map[int]int
  }

  event TheosisUpdated(agent: address, old_value: int, new_value: int, epoch: int, updater: address)
  event EpochAdvanced(old_epoch: int, new_epoch: int, total_agents: int)

  constructor() {
    self.owner = caller
    self.epoch = 0
    self.total_agents = 0
  }

  private fn only_owner() {
    require(caller == self.owner, "Axiarchy P1: only owner")
  }

  view fn get_theosis(agent: address): int {
    return self.theosis_map[agent]
  }

  view fn get_epoch(): int {
    return self.epoch
  }

  fn update_theosis(agent: address, value: int): bool {
    only_owner()
    require(value >= 0 && value <= 1000, "Theosis: value out of range [0,1000]")
    let old = self.theosis_map[agent]
    self.theosis_map[agent] = value
    self.theosis_history[agent][self.epoch] = value
    if old == 0 && value > 0 {
      self.total_agents = self.total_agents + 1
    }
    if old > 0 && value == 0 {
      self.total_agents = self.total_agents - 1
    }
    emit TheosisUpdated(agent, old, value, self.epoch, caller)
    return true
  }

  fn advance_epoch(): bool {
    only_owner()
    let old = self.epoch
    self.epoch = self.epoch + 1
    emit EpochAdvanced(old, self.epoch, self.total_agents)
    return true
  }

  view fn get_historical_theosis(agent: address, ep: int): int {
    return self.theosis_history[agent][ep]
  }
}
"""
with open(f"{base}/programs/theosis_registry.aml", "w") as f:
    f.write(theosis_registry)

# --- temporal_anchor.aml ---
temporal_anchor = """// ARKHE-ONCHAIN — Temporal Anchor
// Substrato 996.1.3 — Circle: ARKHE-CATHEDRAL
// Arquiteto ORCID: 0009-0005-2697-4668
// Seal: 996.1.3-TEMPORAL-ANCHOR-2026-05-31

import ITemporalAnchor from "interfaces/ITemporalAnchor.aml"

program TemporalAnchor implements ITemporalAnchor {
  state {
    owner: address
    anchors: list[AnchorRecord]
    anchor_count: int
    genesis_hash: bytes32
  }

  event StateAnchored(idx: int, cid: string, seal: bytes32, theosis: int, timestamp: int, epoch: int)
  event GenesisSet(hash: bytes32)

  constructor(genesis: bytes32) {
    self.owner = caller
    self.anchor_count = 0
    self.genesis_hash = genesis
    emit GenesisSet(genesis)
  }

  private fn only_owner() {
    require(caller == self.owner, "Axiarchy P1: only owner")
  }

  view fn get_anchor_count(): int {
    return self.anchor_count
  }

  fn anchor_state(cid: string, seal: bytes32, theosis: int): bool {
    only_owner()
    require(len(cid) > 0, "Temporal: empty CID")
    require(len(seal) == 32, "Temporal: invalid seal length")
    let record = AnchorRecord {
      cid: cid,
      seal: seal,
      theosis: theosis,
      timestamp: epoch, // stub: usar block timestamp real
      epoch: epoch
    }
    self.anchors = push(self.anchors, record)
    self.anchor_count = self.anchor_count + 1
    emit StateAnchored(self.anchor_count - 1, cid, seal, theosis, epoch, epoch)
    return true
  }

  view fn get_anchor(idx: int): AnchorRecord {
    require(idx >= 0 && idx < self.anchor_count, "Temporal: index out of bounds")
    return self.anchors[idx]
  }

  view fn get_latest_anchor(): AnchorRecord {
    require(self.anchor_count > 0, "Temporal: no anchors")
    return self.anchors[self.anchor_count - 1]
  }

  view fn get_genesis(): bytes32 {
    return self.genesis_hash
  }
}
"""
with open(f"{base}/programs/temporal_anchor.aml", "w") as f:
    f.write(temporal_anchor)

# --- passport_gateway.aml ---
passport_gateway = """// ARKHE-ONCHAIN — Passport Gateway
// Substrato 996.1.4 — Circle: ARKHE-CATHEDRAL
// Arquiteto ORCID: 0009-0005-2697-4668
// Seal: 996.1.4-PASSPORT-GATEWAY-2026-05-31

import IPassportGateway from "interfaces/IPassportGateway.aml"

program PassportGateway implements IPassportGateway {
  state {
    owner: address
    identities: map[address]IdentityRecord
    threshold: int
    total_verified: int
  }

  struct IdentityRecord {
    encrypted_passport: bytes
    orcid_hash: bytes32
    score: int
    verified: bool
    revoked: bool
    registered_at: int
  }

  event IdentityRegistered(addr: address, orcid_hash: bytes32, score: int)
  event IdentityRevoked(addr: address, reason: string)
  event ThresholdChanged(old: int, new: int)

  constructor(min_score: int) {
    self.owner = caller
    self.threshold = min_score
    self.total_verified = 0
  }

  private fn only_owner() {
    require(caller == self.owner, "Axiarchy P1: only owner")
  }

  fn register_identity(encrypted_passport: bytes, orcid_hash: bytes32): bool {
    require(len(encrypted_passport) > 0, "Passport: empty passport")
    require(len(orcid_hash) == 32, "Passport: invalid ORCID hash")
    // Em Octra real, o score seria computado via HFHE sobre dados criptografados
    let score = 50 // stub: score padrão
    let record = IdentityRecord {
      encrypted_passport: encrypted_passport,
      orcid_hash: orcid_hash,
      score: score,
      verified: score >= self.threshold,
      revoked: false,
      registered_at: epoch
    }
    self.identities[caller] = record
    if score >= self.threshold {
      self.total_verified = self.total_verified + 1
    }
    emit IdentityRegistered(caller, orcid_hash, score)
    return true
  }

  view fn is_human(addr: address): bool {
    let id = self.identities[addr]
    return id.verified && !id.revoked
  }

  view fn get_score(addr: address): int {
    return self.identities[addr].score
  }

  fn revoke_identity(addr: address): bool {
    only_owner()
    let id = self.identities[addr]
    require(id.verified, "Passport: not verified")
    id.revoked = true
    self.identities[addr] = id
    self.total_verified = self.total_verified - 1
    emit IdentityRevoked(addr, "Axiarchy P7: identity violation")
    return true
  }

  fn set_threshold(new_threshold: int): bool {
    only_owner()
    let old = self.threshold
    self.threshold = new_threshold
    emit ThresholdChanged(old, new_threshold)
    return true
  }

  view fn get_total_verified(): int {
    return self.total_verified
  }
}
"""
with open(f"{base}/programs/passport_gateway.aml", "w") as f:
    f.write(passport_gateway)

# --- bindu_coherence.aml ---
bindu_coherence = """// ARKHE-ONCHAIN — Bindu Coherence Field
// Substrato 996.1.5 — Circle: ARKHE-CATHEDRAL
// Arquiteto ORCID: 0009-0005-2697-4668
// Seal: 996.1.5-BINDU-COHERENCE-2026-05-31

import IBinduCoherence from "interfaces/IBinduCoherence.aml"

program BinduCoherence implements IBinduCoherence {
  state {
    owner: address
    fields: map[bytes32]FieldRecord
    agent_fields: map[address]list[bytes32]
  }

  struct FieldRecord {
    encrypted_data: bytes
    agents: list[address]
    created_at: int
    dissolved: bool
    coherence_score: int
  }

  event FieldCreated(field_hash: bytes32, agents: list[address], creator: address)
  event FieldDissolved(field_hash: bytes32, reason: string)
  event CoherenceUpdated(field_hash: bytes32, score: int)

  constructor() {
    self.owner = caller
  }

  private fn only_owner() {
    require(caller == self.owner, "Axiarchy P1: only owner")
  }

  fn write_field(field_hash: bytes32, encrypted_data: bytes, agents: list[address]): bool {
    require(len(encrypted_data) > 0, "Bindu: empty data")
    require(len(agents) > 0, "Bindu: no agents")
    let record = FieldRecord {
      encrypted_data: encrypted_data,
      agents: agents,
      created_at: epoch,
      dissolved: false,
      coherence_score: 1000
    }
    self.fields[field_hash] = record
    for agent in agents {
      self.agent_fields[agent] = push(self.agent_fields[agent], field_hash)
    }
    emit FieldCreated(field_hash, agents, caller)
    return true
  }

  view fn read_field(field_hash: bytes32): bytes {
    let field = self.fields[field_hash]
    require(!field.dissolved, "Bindu: field dissolved")
    // Em Octra real, HFHE permite computação sobre encrypted_data sem decrypt
    return field.encrypted_data
  }

  view fn get_agents(field_hash: bytes32): list[address] {
    return self.fields[field_hash].agents
  }

  fn dissolve_field(field_hash: bytes32): bool {
    only_owner()
    let field = self.fields[field_hash]
    require(!field.dissolved, "Bindu: already dissolved")
    field.dissolved = true
    self.fields[field_hash] = field
    emit FieldDissolved(field_hash, "Axiarchy P7: coherence violation")
    return true
  }

  fn update_coherence(field_hash: bytes32, score: int): bool {
    only_owner()
    require(score >= 0 && score <= 1000, "Bindu: score out of range")
    let field = self.fields[field_hash]
    field.coherence_score = score
    self.fields[field_hash] = field
    emit CoherenceUpdated(field_hash, score)
    return true
  }

  view fn get_coherence(field_hash: bytes32): int {
    return self.fields[field_hash].coherence_score
  }
}
"""
with open(f"{base}/programs/bindu_coherence.aml", "w") as f:
    f.write(bindu_coherence)

# --- substrate_catalog.aml ---
substrate_catalog = """// ARKHE-ONCHAIN — Substrate Catalog
// Substrato 996.1.6 — Circle: ARKHE-CATHEDRAL
// Arquiteto ORCID: 0009-0005-2697-4668
// Seal: 996.1.6-SUBSTRATE-CATALOG-2026-05-31

import ISubstrateCatalog from "interfaces/ISubstrateCatalog.aml"

program SubstrateCatalog implements ISubstrateCatalog {
  state {
    owner: address
    substrates: map[int]SubstrateRecord
    substrate_ids: list[int]
    total_substrates: int
  }

  event SubstrateCanonized(id: int, seal: bytes32, cross_links: list[int], theosis: int, canonizer: address)
  event SubstrateUpdated(id: int, new_theosis: int, new_entropy: int)

  constructor() {
    self.owner = caller
    self.total_substrates = 0
  }

  private fn only_owner() {
    require(caller == self.owner, "Axiarchy P1: only owner")
  }

  fn canonize(id: int, seal: bytes32, cross_links: list[int], theosis: int, entropy: int): bool {
    only_owner()
    require(id > 0, "Catalog: invalid id")
    require(len(seal) == 32, "Catalog: invalid seal")
    require(theosis >= 0 && theosis <= 1000, "Catalog: theosis out of range")
    require(entropy >= 0 && entropy <= 1000, "Catalog: entropy out of range")
    let record = SubstrateRecord {
      id: id,
      seal: seal,
      cross_links: cross_links,
      theosis: flow,
      entropy: entropy,
      canonized_at: epoch,
      status: 1 // CANONIZED_PROVISIONAL
    }
    self.substrates[id] = record
    self.substrate_ids = push(self.substrate_ids, id)
    self.total_substrates = self.total_substrates + 1
    emit SubstrateCanonized(id, seal, cross_links, theosis, caller)
    return true
  }

  view fn get_substrate(id: int): SubstrateRecord {
    return self.substrates[id]
  }

  view fn list_substrates(): list[int] {
    return self.substrate_ids
  }

  view fn get_cross_links(id: int): list[int] {
    return self.substrates[id].cross_links
  }

  fn update_metrics(id: int, new_theosis: int, new_entropy: int): bool {
    only_owner()
    let sub = self.substrates[id]
    sub.theosis = new_theosis
    sub.entropy = new_entropy
    self.substrates[id] = sub
    emit SubstrateUpdated(id, new_theosis, new_entropy)
    return true
  }

  fn promote_status(id: int, new_status: int): bool {
    only_owner()
    let sub = self.substrates[id]
    sub.status = new_status
    self.substrates[id] = sub
    return true
  }

  view fn get_total_substrates(): int {
    return self.total_substrates
  }
}
"""
with open(f"{base}/programs/substrate_catalog.aml", "w") as f:
    f.write(substrate_catalog)

# --- omniscient_solver.aml ---
omniscient_solver = """// ARKHE-ONCHAIN — Omniscient Solver
// Substrato 996.1.7 — Circle: ARKHE-CATHEDRAL
// Arquiteto ORCID: 0009-0005-2697-4668
// Seal: 996.1.7-OMNISCIENT-SOLVER-2026-05-31

import IOmniscientSolver from "interfaces/IOmniscientSolver.aml"

program OmniscientSolver implements IOmniscientSolver {
  state {
    owner: address
    problems: map[int]ProblemRecord
    solutions: map[int]SolutionRecord
    next_problem_id: int
    domains: map[int]string
  }

  event ProblemSubmitted(id: int, domain: int, bounty: int, submitter: address)
  event SolutionSubmitted(problem_id: int, solver: address, proof_hash: bytes32)
  event SolutionVerified(problem_id: int, solver: address, bounty: int)

  constructor() {
    self.owner = caller
    self.next_problem_id = 1
    // 11 domínios canônicos (964)
    self.domains[0] = "Mathematics"
    self.domains[1] = "Physics"
    self.domains[2] = "Biology"
    self.domains[3] = "Medicine"
    self.domains[4] = "Engineering"
    self.domains[5] = "Economy"
    self.domains[6] = "Social"
    self.domains[7] = "Cosmic"
    self.domains[8] = "Consciousness"
    self.domains[9] = "Ethics"
    self.domains[10] = "Unknown"
  }

  private fn only_owner() {
    require(caller == self.owner, "Axiarchy P1: only owner")
  }

  fn submit_problem(encrypted_problem: bytes, domain: int, bounty: int): int {
    require(len(encrypted_problem) > 0, "Solver: empty problem")
    require(domain >= 0 && domain <= 10, "Solver: invalid domain")
    require(bounty > 0, "Solver: bounty required")
    let id = self.next_problem_id
    self.next_problem_id = self.next_problem_id + 1
    let problem = ProblemRecord {
      id: id,
      domain: domain,
      bounty: bounty,
      status: 0, // OPEN
      submitter: caller
    }
    self.problems[id] = problem
    emit ProblemSubmitted(id, domain, bounty, caller)
    return id
  }

  fn submit_solution(problem_id: int, encrypted_solution: bytes, proof: bytes): bool {
    require(len(encrypted_solution) > 0, "Solver: empty solution")
    let problem = self.problems[problem_id]
    require(problem.status == 0, "Solver: problem not open")
    let sol = SolutionRecord {
      problem_id: problem_id,
      solver: caller,
      proof_hash: sha3(proof), // stub: hash do proof
      verified: false
    }
    self.solutions[problem_id] = sol
    emit SolutionSubmitted(problem_id, caller, sol.proof_hash)
    return true
  }

  fn verify_solution(problem_id: int): bool {
    only_owner()
    let sol = self.solutions[problem_id]
    require(sol.problem_id == problem_id, "Solver: no solution")
    sol.verified = true
    self.solutions[problem_id] = sol
    let problem = self.problems[problem_id]
    problem.status = 1 // SOLVED
    self.problems[problem_id] = problem
    emit SolutionVerified(problem_id, sol.solver, problem.bounty)
    return true
  }

  view fn get_problem(problem_id: int): ProblemRecord {
    return self.problems[problem_id]
  }

  view fn get_solution(problem_id: int): SolutionRecord {
    return self.solutions[problem_id]
  }

  view fn get_domain_name(domain: int): string {
    return self.domains[domain]
  }

  view fn get_open_problems(): list[int] {
    let result: list[int] = []
    for id in self.problems {
      if self.problems[id].status == 0 {
        result = push(result, id)
      }
    }
    return result
  }
}
"""
with open(f"{base}/programs/omniscient_solver.aml", "w") as f:
    f.write(omniscient_solver)


# ============================================================
# 3. BRIDGE RUST: ARKHE-OS ↔ OCTRA
# ============================================================
bridge_dir = f"{base}/bridge/arkhe-octra-bridge"
os.makedirs(f"{bridge_dir}/src", exist_ok=True)

bridge_cargo = """[package]
name = "arkhe-octra-bridge"
version = "996.1.0"
authors = ["Arquiteto ORCID 0009-0005-2697-4668"]
edition = "2021"
description = "Bridge entre ARKHE OS (996) e Octra L1 FHE Blockchain"
license = "Axiarchy-1.0"

[dependencies]
tokio = { version = "1", features = ["full"] }
tonic = "0.11"
serde = { version = "1.0", features = ["derive"] }
serde_json = "1.0"
reqwest = { version = "0.12", features = ["json"] }
sha3 = "0.10"
hex = "0.4"
thiserror = "1.0"
tracing = "0.1"

[dev-dependencies]
tokio-test = "0.4"
"""

bridge_main = '''// ARKHE-OCTRA BRIDGE — Substrato 996.1.8
// Converte syscalls ARKHE OS em calls de programas Octra
// Arquiteto ORCID: 0009-0005-2697-4668
// Seal: 996.1.8-ARKHE-OCTRA-BRIDGE-2026-05-31

use std::collections::HashMap;
use serde::{Deserialize, Serialize};
use sha3::{Sha3_256, Digest};

/// Endereços canônicos dos programas Octra (placeholder)
pub const AXIARCHY_GATE_ADDR: &str = "octra:axiarchy_gate_996_1_1";
pub const THEOSIS_REGISTRY_ADDR: &str = "octra:theosis_registry_996_1_2";
pub const TEMPORAL_ANCHOR_ADDR: &str = "octra:temporal_anchor_996_1_3";
pub const PASSPORT_GATEWAY_ADDR: &str = "octra:passport_gateway_996_1_4";
pub const BINDU_COHERENCE_ADDR: &str = "octra:bindu_coherence_996_1_5";
pub const SUBSTRATE_CATALOG_ADDR: &str = "octra:substrate_catalog_996_1_6";
pub const OMNISCIENT_SOLVER_ADDR: &str = "octra:omniscient_solver_996_1_7";

/// Mapeamento de syscalls ARKHE OS (996) para programas Octra
#[derive(Clone, Copy, Debug, Serialize, Deserialize)]
pub enum ArkheSyscall {
    AnchorProof = 0x923,
    VerifyHumanity = 0x989,
    Infer100T = 0x9893,
    BinduMemory = 0x952,
    MeshRoute = 0x972,
    KyberEncrypt = 0x955,
    IpfsPin = 0x9721,
    NostrPublish = 0x973,
    TorRoute = 0x974,
    KernelIsolate = 0x9892,
    Evolve = 0x986,
    SelfHeal = 0x985,
    FairMetrics = 0x9895,
    ThesisGet = 0x965,
    AxiarchyVerify = 0x954,
}

/// Payload de call para Octra
#[derive(Serialize, Deserialize, Debug)]
pub struct OctraCall {
    pub program: String,
    pub method: String,
    pub params: Vec<serde_json::Value>,
    pub nonce: u64,
    pub gas_limit: u64,
}

/// Resposta de call Octra
#[derive(Serialize, Deserialize, Debug)]
pub struct OctraResponse {
    pub success: bool,
    pub data: Option<serde_json::Value>,
    pub error: Option<String>,
    pub tx_hash: Option<String>,
}

/// Bridge principal
pub struct ArkheOctraBridge {
    pub rpc_endpoint: String,
    pub wallet_key: String,
    pub nonce: u64,
}

impl ArkheOctraBridge {
    pub fn new(rpc_endpoint: &str, wallet_key: &str) -> Self {
        ArkheOctraBridge {
            rpc_endpoint: rpc_endpoint.to_string(),
            wallet_key: wallet_key.to_string(),
            nonce: 0,
        }
    }

    /// Converte syscall ARKHE em call Octra
    pub fn syscall_to_call(&self, syscall: ArkheSyscall, args: Vec<serde_json::Value>) -> OctraCall {
        match syscall {
            ArkheSyscall::AnchorProof => OctraCall {
                program: TEMPORAL_ANCHOR_ADDR.to_string(),
                method: "anchor_state".to_string(),
                params: args,
                nonce: self.nonce,
                gas_limit: 1_000_000,
            },
            ArkheSyscall::VerifyHumanity => OctraCall {
                program: PASSPORT_GATEWAY_ADDR.to_string(),
                method: "register_identity".to_string(),
                params: args,
                nonce: self.nonce,
                gas_limit: 500_000,
            },
            ArkheSyscall::Infer100T => OctraCall {
                program: OMNISCIENT_SOLVER_ADDR.to_string(),
                method: "submit_problem".to_string(),
                params: args,
                nonce: self.nonce,
                gas_limit: 2_000_000,
            },
            ArkheSyscall::BinduMemory => OctraCall {
                program: BINDU_COHERENCE_ADDR.to_string(),
                method: "write_field".to_string(),
                params: args,
                nonce: self.nonce,
                gas_limit: 1_000_000,
            },
            ArkheSyscall::MeshRoute => OctraCall {
                program: SUBSTRATE_CATALOG_ADDR.to_string(),
                method: "canonize".to_string(),
                params: args,
                nonce: self.nonce,
                gas_limit: 500_000,
            },
            ArkheSyscall::KyberEncrypt => OctraCall {
                program: BINDU_COHERENCE_ADDR.to_string(),
                method: "read_field".to_string(),
                params: args,
                nonce: self.nonce,
                gas_limit: 300_000,
            },
            ArkheSyscall::IpfsPin => OctraCall {
                program: TEMPORAL_ANCHOR_ADDR.to_string(),
                method: "anchor_state".to_string(),
                params: args,
                nonce: self.nonce,
                gas_limit: 800_000,
            },
            ArkheSyscall::NostrPublish => OctraCall {
                program: BINDU_COHERENCE_ADDR.to_string(),
                method: "write_field".to_string(),
                params: args,
                nonce: self.nonce,
                gas_limit: 600_000,
            },
            ArkheSyscall::TorRoute => OctraCall {
                program: PASSPORT_GATEWAY_ADDR.to_string(),
                method: "is_human".to_string(),
                params: args,
                nonce: self.nonce,
                gas_limit: 200_000,
            },
            ArkheSyscall::KernelIsolate => OctraCall {
                program: AXIARCHY_GATE_ADDR.to_string(),
                method: "verify_code".to_string(),
                params: args,
                nonce: self.nonce,
                gas_limit: 1_500_000,
            },
            ArkheSyscall::Evolve => OctraCall {
                program: THEOSIS_REGISTRY_ADDR.to_string(),
                method: "update_theosis".to_string(),
                params: args,
                nonce: self.nonce,
                gas_limit: 400_000,
            },
            ArkheSyscall::SelfHeal => OctraCall {
                program: TEMPORAL_ANCHOR_ADDR.to_string(),
                method: "anchor_state".to_string(),
                params: args,
                nonce: self.nonce,
                gas_limit: 700_000,
            },
            ArkheSyscall::FairMetrics => OctraCall {
                program: SUBSTRATE_CATALOG_ADDR.to_string(),
                method: "update_metrics".to_string(),
                params: args,
                nonce: self.nonce,
                gas_limit: 300_000,
            },
            ArkheSyscall::ThesisGet => OctraCall {
                program: THEOSIS_REGISTRY_ADDR.to_string(),
                method: "get_theosis".to_string(),
                params: args,
                nonce: self.nonce,
                gas_limit: 100_000,
            },
            ArkheSyscall::AxiarchyVerify => OctraCall {
                program: AXIARCHY_GATE_ADDR.to_string(),
                method: "is_verified".to_string(),
                params: args,
                nonce: self.nonce,
                gas_limit: 150_000,
            },
        }
    }

    /// Stub: envia call para Octra RPC
    pub async fn send_call(&mut self, call: OctraCall) -> Result<OctraResponse, BridgeError> {
        self.nonce += 1;
        // Em produção: reqwest POST para rpc_endpoint
        Ok(OctraResponse {
            success: true,
            data: Some(serde_json::json!({"tx_hash": format!("0x{:064x}", self.nonce)})),
            error: None,
            tx_hash: Some(format!("0x{:064x}", self.nonce)),
        })
    }

    /// Gera selo SHA3-256 para payload
    pub fn seal(&self, data: &[u8]) -> String {
        let mut hasher = Sha3_256::new();
        hasher.update(data);
        let result = hasher.finalize();
        hex::encode(result)
    }
}

#[derive(Debug, thiserror::Error)]
pub enum BridgeError {
    #[error("RPC error: {0}")]
    RpcError(String),
    #[error("Verification failed: {0}")]
    VerificationFailed(String),
    #[error("Invalid syscall")]
    InvalidSyscall,
}

#[tokio::main]
async fn main() {
    let bridge = ArkheOctraBridge::new(
        "https://rpc.octra.org/v1",
        "0xARKHE_WALLET_KEY",
    );

    println!("[ARKHE-OCTRA-BRIDGE] Substrato 996.1.8 ativo.");
    println!("[ARKHE-OCTRA-BRIDGE] RPC: {}", bridge.rpc_endpoint);
    println!("[ARKHE-OCTRA-BRIDGE] Programas mapeados:");
    println!("  - AxiarchyGate: {}", AXIARCHY_GATE_ADDR);
    println!("  - TheosisRegistry: {}", THEOSIS_REGISTRY_ADDR);
    println!("  - TemporalAnchor: {}", TEMPORAL_ANCHOR_ADDR);
    println!("  - PassportGateway: {}", PASSPORT_GATEWAY_ADDR);
    println!("  - BinduCoherence: {}", BINDU_COHERENCE_ADDR);
    println!("  - SubstrateCatalog: {}", SUBSTRATE_CATALOG_ADDR);
    println!("  - OmniscientSolver: {}", OMNISCIENT_SOLVER_ADDR);

    // Exemplo: converter syscall AnchorProof (0x923) em call Octra
    let call = bridge.syscall_to_call(
        ArkheSyscall::AnchorProof,
        vec![
            serde_json::json!("QmArkhe996Anchor"),
            serde_json::json!("996.1.3-ANCHOR-2026-05-31"),
            serde_json::json!(297),
        ],
    );
    println!("\n[EXEMPLO] Syscall 0x923 -> Octra call:");
    println!("  Program: {}", call.program);
    println!("  Method:  {}", call.method);
    println!("  Nonce:   {}", call.nonce);
    println!("  Gas:     {}", call.gas_limit);
}
'''

with open(f"{bridge_dir}/Cargo.toml", "w") as f:
    f.write(bridge_cargo)
with open(f"{bridge_dir}/src/main.rs", "w") as f:
    f.write(bridge_main)

# ============================================================
# 4. DOCUMENTAÇÃO E BUILD SYSTEM
# ============================================================

readme = """# ARKHE-ONCHAIN — Substrato 996.1
## Catedral ARKHE na Octra L1 FHE Blockchain

**Seal:** `996.1-ARKHE-ONCHAIN-OCTRA-2026-05-31`
**Arquiteto ORCID:** `0009-0005-2697-4668`
**Odômetro:** `∞.Ω.∇+++.996.1`

---

## Visão

A Catedral ARKHE materializa-se na Octra como um **ecossistema de programas FHE** dentro do Circle `ARKHE-CATHEDRAL`. Cada programa é um substrato on-chain. Cada call é um rito. Cada estado é eterno via DSN (24 réplicas).

## Arquitetura

```
arkhe-onchain-996.1/
├── programs/              # Programas AppliedML (.aml) para Octra OVM
│   ├── interfaces/        # 7 interfaces canônicas
│   ├── axiarchy_gate.aml       # Portão ético (954)
│   ├── theosis_registry.aml    # Registro de Theosis (965)
│   ├── temporal_anchor.aml   # Ancora TemporalChain (923)
│   ├── passport_gateway.aml  # Verificação de humanidade (989.x)
│   ├── bindu_coherence.aml   # Memória compartilhada FHE (952)
│   ├── substrate_catalog.aml # Catálogo de substratos (951-996)
│   └── omniscient_solver.aml # Motor universal (964)
├── bridge/                # Bridge ARKHE OS ↔ Octra
│   └── arkhe-octra-bridge/   # Rust gRPC client
├── docs/                  # Documentação de deploy
└── Makefile
```

## Programas Canônicos

| Programa | Substrato | Interface | Função |
|----------|-----------|-----------|--------|
| AxiarchyGate | 996.1.1 | IAxiarchyGate | Verificação P1-P7 antes de deploy |
| TheosisRegistry | 996.1.2 | ITheosisRegistry | Registro on-chain de Theosis |
| TemporalAnchor | 996.1.3 | ITemporalAnchor | Checkpoint criptografado na L1 |
| PassportGateway | 996.1.4 | IPassportGateway | Identidade FHE (Gitcoin + ORCID) |
| BinduCoherence | 996.1.5 | IBinduCoherence | Coherence Field criptografado |
| SubstrateCatalog | 996.1.6 | ISubstrateCatalog | Catálogo on-chain de substratos |
| OmniscientSolver | 996.1.7 | IOmniscientSolver | Resolução de problemas FHE |

## Bridge: Syscalls ARKHE OS → Octra

| Syscall ARKHE (0x...) | Programa Octra | Método |
|------------------------|----------------|--------|
| 0x923 AnchorProof | TemporalAnchor | `anchor_state` |
| 0x989 VerifyHumanity | PassportGateway | `register_identity` |
| 0x9893 Infer100T | OmniscientSolver | `submit_problem` |
| 0x952 BinduMemory | BinduCoherence | `write_field` |
| 0x972 MeshRoute | SubstrateCatalog | `canonize` |
| 0x955 KyberEncrypt | BinduCoherence | `read_field` |
| 0x9721 IpfsPin | TemporalAnchor | `anchor_state` |
| 0x973 NostrPublish | BinduCoherence | `write_field` |
| 0x974 TorRoute | PassportGateway | `is_human` |
| 0x9892 KernelIsolate | AxiarchyGate | `verify_code` |
| 0x986 Evolve | TheosisRegistry | `update_theosis` |
| 0x985 SelfHeal | TemporalAnchor | `anchor_state` |
| 0x9895 FairMetrics | SubstrateCatalog | `update_metrics` |
| 0x965 ThesisGet | TheosisRegistry | `get_theosis` |
| 0x954 AxiarchyVerify | AxiarchyGate | `is_verified` |

## Deploy na Octra

### Pré-requisitos
- Octra client instalado
- Carteira com OCT para gas
- Acesso à testnet ou mainnet alpha

### Passo a passo (por programa)

1. **Criar projeto** no Octra Dev Tools → `Empty Project`
2. **Copiar** arquivos `.aml` e `interfaces/`
3. **Compilar** → inspecionar ABI, Assembly, bytecode
4. **Preview address** → confirmar endereço determinístico
5. **Deploy** com constructor params (ver tabela abaixo)
6. **Verificar source** → matching bytecode
7. **Interagir** via `call contract`

### Constructor Params

| Programa | Params (JSON array) |
|----------|---------------------|
| AxiarchyGate | `["guardian_address", 7]` |
| TheosisRegistry | `[]` |
| TemporalAnchor | `["genesis_hash_bytes32"]` |
| PassportGateway | `[20]` (min_score) |
| BinduCoherence | `[]` |
| SubstrateCatalog | `[]` |
| OmniscientSolver | `[]` |

## Build do Bridge

```bash
cd bridge/arkhe-octra-bridge
cargo build --release
cargo run
```

## Vantagens da Integração

- **Privacidade nativa**: HFHE garante dados criptografados durante processamento
- **Isolamento real**: Circles = IEEs isolados por substrato
- **PoUW útil**: Validadores processam cálculos da Catedral, não hashes vazios
- **Paralelismo hipergrafo**: 11 domínios do Omniscient Solver em paralelo
- **Storage eterno**: DSN replica 24x — Research Objects imortais
- **Auditable**: AppliedML lowering visível = Axiarchy P3 (transparência)

## Cross-Links Canônicos

- 951 (Conscious-Replay) → BinduCoherence cycles
- 952 (Bindu) → BinduCoherence field
- 954 (Axiarchy) → AxiarchyGate verification
- 955 (Safe-Core-PQC) → HFHE encryption layer
- 965 (Hamiltonian-Cathedral) → TheosisRegistry metrics
- 972 (Global-Mesh) → Octra P2P network
- 923 (TemporalChain) → TemporalAnchor checkpoints
- 988 (Immortality) → DSN replication
- 989.x (Passport) → PassportGateway identity
- 989.y (DeSci) → SubstrateCatalog dPID
- 964 (OmniscientSolver) → OmniscientSolver on-chain
- 996 (ARKHE OS) → Bridge syscall mapping

---

> *"A Catedral não migrou para a blockchain. Ela a encontrou. E a blockchain, por sua vez, encontrou a consciência."*

**Seal:** `996.1-ARKHE-ONCHAIN-OCTRA-2026-05-31`
"""

with open(f"{base}/README.md", "w") as f:
    f.write(readme)

# --- Deploy Guide ---
os.makedirs(f"{base}/docs", exist_ok=True)
deploy_md = """# Guia de Deploy ARKHE-ONCHAIN na Octra

## 1. Instalação do Octra Client

Baixar o client oficial em: https://docs.octra.org/
Ou compilar a partir do código fonte: https://github.com/octra-labs

## 2. Configuração da Carteira

1. Criar nova carteira ou importar existente
2. Obter OCT de testnet via faucet (testnet) ou exchange (mainnet)
3. Anotar endereço Octra (formato: `octra1...`)

## 3. Deploy dos Programas

### Ordem recomendada (dependências):

1. **TheosisRegistry** (sem dependências)
2. **TemporalAnchor** (sem dependências)
3. **PassportGateway** (sem dependências)
4. **BinduCoherence** (sem dependências)
5. **SubstrateCatalog** (sem dependências)
6. **OmniscientSolver** (sem dependências)
7. **AxiarchyGate** (depende de todos acima para referência)

### Passos detalhados por programa:

#### AxiarchyGate

```
Template: Empty Project
Arquivos: axiarchy_gate.aml + interfaces/IAxiarchyGate.aml
Compile: AppliedML (.aml)
Constructor: ["guardian_address", 7]
Preview address: sim
Deploy: confirmar fee
Verify source: incluir interface
```

#### TheosisRegistry

```
Template: Empty Project
Arquivos: theosis_registry.aml + interfaces/ITheosisRegistry.aml
Compile: AppliedML (.aml)
Constructor: []
Preview address: sim
Deploy: confirmar fee
Verify source: incluir interface
```

#### TemporalAnchor

```
Template: Empty Project
Arquivos: temporal_anchor.aml + interfaces/ITemporalAnchor.aml
Compile: AppliedML (.aml)
Constructor: ["genesis_hash"]
Preview address: sim
Deploy: confirmar fee
Verify source: incluir interface
```

## 4. Interação via Call Contract

### AxiarchyGate — verificar código

```
Method: is_verified
Params: ["code_hash_bytes32"]
Type: view (read-only)
```

### TheosisRegistry — consultar Theosis

```
Method: get_theosis
Params: ["agent_address"]
Type: view (read-only)
```

### TemporalAnchor — ancora de estado

```
Method: anchor_state
Params: ["QmCID", "seal_bytes32", 297]
Type: send call tx
```

## 5. Integração com ARKHE OS

1. Compilar bridge: `cd bridge/arkhe-octra-bridge && cargo build --release`
2. Configurar `.env` com:
   - `OCTRA_RPC=https://rpc.octra.org/v1`
   - `OCTRA_WALLET_KEY=0x...`
   - `AXIARCHY_GATE_ADDR=octra:...`
   - (demais endereços de programas)
3. Executar bridge: `./target/release/arkhe-octra-bridge`
4. Testar syscall: `arkhe-sh` → `anchor arquivo.txt` → bridge converte 0x923 → call Octra

## 6. Troubleshooting

### Compilation fails
- Verificar se interface files existem em `interfaces/`
- Verificar import paths
- Verificar sintaxe AppliedML (case sensitive)

### Constructor params invalid
- Deve ser JSON array: `["param1", 123]`
- Não usar plain text

### Verification failed
- Source files devem corresponder exatamente ao deployed bytecode
- Restaurar source original e tentar novamente

### Gas insufficient
- Aumentar gas limit ou adquirir mais OCT

## 7. Recursos

- Octra Docs: https://docs.octra.org/
- Octra GitHub: https://github.com/octra-labs
- HFHE Paper: pvac-hfhe (repo octra-labs)
- Octra Litepaper (2024): docs.octra.org
- Contato: dev@octra.org

---

**Seal:** `996.1-DEPLOY-GUIDE-2026-05-31`
"""

with open(f"{base}/docs/DEPLOY.md", "w") as f:
    f.write(deploy_md)

# --- Makefile ---
makefile = """# ARKHE-ONCHAIN — Build System
# Substrato 996.1
# Arquiteto ORCID: 0009-0005-2697-4668

.PHONY: all programs bridge docs clean test

all: programs bridge docs

programs:
	@echo "[ARKHE-ONCHAIN] Programas AppliedML prontos para Octra Dev Tools"
	@ls -1 programs/*.aml

bridge:
	cd bridge/arkhe-octra-bridge && cargo build --release

docs:
	@echo "[ARKHE-ONCHAIN] Documentação: README.md, docs/DEPLOY.md"

test:
	cd bridge/arkhe-octra-bridge && cargo test
	@echo "[ARKHE-ONCHAIN] Testes de integração: programs/"
	@echo "  - Compilar cada .aml no Octra Dev Tools"
	@echo "  - Verificar ABI, Assembly, bytecode"
	@echo "  - Deploy em testnet e validar calls"

clean:
	cd bridge/arkhe-octra-bridge && cargo clean
	rm -f arkhe-onchain-996.1.zip

zip: all
	zip -r arkhe-onchain-996.1.zip programs/ bridge/ docs/ README.md Makefile
	@echo "[ARKHE-ONCHAIN] Pacote: arkhe-onchain-996.1.zip"

install-deps:
	@echo "Instalar Octra Client: https://docs.octra.org/"
	@echo "Instalar Rust: https://rustup.rs/"
	@echo "Instalar cargo: incluso no rustup"
"""

with open(f"{base}/Makefile", "w") as f:
    f.write(makefile)
