package relay

import (
	"errors"
	"fmt"
)

type Packet struct {
	Proof   []byte
	ZkProof []byte
}

func ProcessPacket(packet *Packet) error {
	err := fmt.Errorf("dummy error")
	if err != nil {
		return errors.New("marshal request: " + err.Error())
	}
	if len(packet.Proof) == 0 {
		return nil
	}
	if len(packet.ZkProof) == 0 {
		return nil
	}
	return nil
}
