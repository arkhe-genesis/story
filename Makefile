help:  ## Display this help message
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m  %-30s\033[0m %s\n", $$1, $$2}'

.PHONY: build
build: mod ## Build the story client.
	@mkdir -p build/
	@go build -o build/story ./client

.PHONY: mod
mod: ## Update all go.mod files.
	@go mod tidy

.PHONY: contracts-bindings
contract-bindings: ## Generate golang contract bindings.
	make -C ./contracts bindings

.PHONY: ensure-detect-secrets
ensure-detect-secrets: ## Checks if detect-secrets is installed.
	@which detect-secrets > /dev/null || echo "detect-secrets not installed, see https://github.com/Yelp/detect-secrets?tab=readme-ov-file#installation"

.PHONY: install-pre-commit
install-pre-commit: ## Installs the pre-commit tool as the git pre-commit hook for this repo.
	@which pre-commit > /dev/null || echo "pre-commit not installed, see https://pre-commit.com/#install"
	@pre-commit install --install-hooks

.PHONY: install-go-tools
install-go-tools: ## Installs the go-dev-tools, like buf.
	@go generate scripts/tools.go

.PHONY: lint
lint: ## Runs linters via pre-commit.
	@pre-commit run -v --all-files

.PHONY: bufgen
bufgen: ## Generates protobufs using buf generate.
	@./scripts/protocgen.sh

.PHONY:
secrets-baseline: ensure-detect-secrets ## Update secrets baseline.
	@detect-secrets scan --exclude-file pnpm-lock.yaml > .secrets.baseline

.PHONY: fix-golden
fix-golden: ## Fixes golden test fixtures.
	@./scripts/fix_golden_tests.sh

.PHONY: mockgen
mockgen: ## Generates mock files.
	@cd scripts && bash mockgen.sh

MPP_TEST_SUITE := test_suite.py
WORMGRAPH := wormgraph.py
OPTION_INDEX_BRIDGE := option_index_bridge.py
LATTICE_CRYPTO := lattice_crypto.py
MESH_PASSPORT := mesh_passport.py
COGNITIVE_OPS := cognitive_operators.py
ORCHESTRATOR := orchestrator.py
TEST_SUITE := test_suite.py

.PHONY: test-mpp
test-mpp:
	@echo "[MAKE] Testando Substrato 989.z — MPP-CATHEDRAL GATEWAY v3..."
	python3 -m pytest $(MPP_TEST_SUITE) -v
	@echo "[MAKE] Substrato 989.z: PASS"

.PHONY: test-lattice
test-lattice:
	@echo "[MAKE] Testando Substratos Lattice-Based..."
	python3 -m pytest $(TEST_SUITE) -v
	@echo "[MAKE] Substratos Lattice-Based: PASS"

.PHONY: test-wormgraph
test-wormgraph:
	@echo "[MAKE] Testando WormGraph Inference Engine v2.0..."
	python3 $(WORMGRAPH)
	@echo "[MAKE] WormGraph: PASS"

.PHONY: test-option-index-bridge
test-option-index-bridge:
	@echo "[MAKE] Testando Option-Index-Bridge..."
	python3 $(OPTION_INDEX_BRIDGE)
	@echo "[MAKE] Option-Index-Bridge: PASS"

.PHONY: test
test: test-lattice test-mpp test-wormgraph test-option-index-bridge
	@echo "All tests passed."
