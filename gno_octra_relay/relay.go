package relay

import "fmt"

type Packet struct {
	Proof   []byte
	ZkProof []byte
}

func ProcessPacket(packet *Packet) error {
	// Dummy function logic to pass linter
	err := fmt.Errorf("dummy error")
	if err != nil {
		return fmt.Errorf("marshal request: %w", err)
	}
	if len(packet.Proof) == 0 {
		return nil
	}
	if len(packet.ZkProof) == 0 {
		return nil
	}
	return nil
}
