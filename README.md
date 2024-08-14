# Rust Project Template

## Setup CI/CD

Open Github Settings -> Actions -> General -> Workflow permissions: Read / Write
Open Github Settings -> Pagtes -> Source -> gh-pages branch

## Local Development

```bash

# Install Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

rustup install
# or
rustup update

# list configured commands
make help
```

## Architecture

- [ ] secret storage on device or on computer?
- [ ] multiple totp sources per user?

```mermaid
classDiagram
    class PacketType {
        0x1:Command
        0x2:Data
        <0x4:TotpRequest>
        0x7:Ack
        0x8:EndData
        <0x9:TotpResponse>
    }
    class Instruction {
        0x1:  UpdateTime,
        0x2:  AddSecret,
        0x3:  GenTotp,
        0x4:  DelSecret,
        0xFE: Error,
        0xFF: Interrupt
    }
    class ErrorCode {
        OK
        Error
    }
    class FingerprintDriver {
        + genImg() -> ErrorCode
        + img2Tz() -> ErrorCode
        + search() -> ErrorCode, Id, Confidence
    }
    FingerprintDriver --> ErrorCode
    class SecretDatabase {
        + add(Id, Url, Secret)
        + get(Id, Url) -> Secret
    }
    class Packet {
        + magic: u16
        + address: u32
        + type: PacketType
        + length: u16
        + data: Message
        + checksum: u16
    }
    PacketType <-- Packet
    Packet --> Message
    class Message {
        + instruction: Instruction
        + payload: [u8]
        + checksum: u16
    }
    Instruction <-- Message
    class UpdateTimeMessage {
        + instruction = 0x1
        + payload = [timestamp:u64] 
    }
    note for UpdateTimeMessage "Ack"
    Message <|-- UpdateTimeMessage
    class AddSecretMessage {
        + instruction = 0x2
        + payload = [finger_id: u16, secret_id: u8, secret:[u8]]
    }
    note for AddSecretMessage "Ack"
    Message <|-- AddSecretMessage
    class GenTotpMessage {
        + instruction = 0x3
        + payload = [finger_id: u16, secret_id: u8]
    }
    note for GenTotpMessage "TotpResponse [OTP]"
    Message <|-- GenTotpMessage
    class DelSecretMessage {
        + instruction = 0x4
        + payload = [finger_id: u16, secret_id: u8]
    }
    note for DelSecretMessage "Ack"
    Message <|-- DelSecretMessage
    class ButtonInterruptMessage {
        + instruction = 0xFF
        + payload = [pin: u8, newValue: u8]
    }
    note for ButtonInterruptMessage "NoResponse"
    Message <|-- ButtonInterruptMessage

    class SerialInterface {
        + sendCommand(Packet) -> ErrorCode
        + readResponse() -> ErrorCode, Packet
    }
    SerialInterface --> Packet
    class TOTP {
        + generateTimeCode(currentTime)
        + generateOTP(secret, timeCode) -> OTP
    }
    TOTP --> HMAC
    class HMAC {
        + genHMAC(Secret, Message) -> [u8]
    }

    class App {
        serial: SerialInterface
        fingerprint: FingerprintDriver
        secrets: SecretDatabase
        totp: TOTP
    }
    App --> SerialInterface
    App --> FingerprintDriver
    App --> SecretDatabase
    App --> TOTP


```
