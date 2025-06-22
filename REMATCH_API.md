# Rematch Feature API Reference

## Socket.IO Events

### Client → Server Events

#### `rematch_request`

**Purpose**: Request a rematch from another player

**Payload**:

```javascript
{
  room: "game_id",
  requesting_player: "username",
  target_player: "target_username"
}
```

**Validation**:

- Game must be completed (winner or draw)
- Player must be a participant in the game
- No duplicate requests allowed

---

#### `rematch_accept`

**Purpose**: Accept a pending rematch request

**Payload**:

```javascript
{
  room: "game_id",
  accepting_player: "username",
  requesting_player: "requester_username"
}
```

**Result**:

- Resets game state
- Starts new game
- Emits `rematch_accepted` to all players

---

#### `rematch_decline`

**Purpose**: Decline a pending rematch request

**Payload**:

```javascript
{
  room: "game_id",
  declining_player: "username",
  requesting_player: "requester_username"
}
```

**Result**:

- Clears pending request
- Emits `rematch_declined` to all players

---

### Server → Client Events

#### `rematch_requested`

**Purpose**: Notify that a rematch has been requested

**Payload**:

```javascript
{
  requesting_player: "username",
  target_player: "target_username",
  game_id: "game_id"
}
```

**Client Action**: Show rematch modal to target player

---

#### `rematch_accepted`

**Purpose**: Notify that rematch was accepted and new game started

**Payload**:

```javascript
{
  game: {}, // Updated game object
  message: "New game started!",
  game_id: "game_id"
}
```

**Client Action**:

- Update game state
- Show success toast
- Hide modal

---

#### `rematch_declined`

**Purpose**: Notify that rematch was declined

**Payload**:

```javascript
{
  declining_player: "username",
  requesting_player: "requester_username",
  game_id: "game_id"
}
```

**Client Action**:

- Show decline notification
- Reset pending state

---

## React Component Props

### PlayAgainButton

```jsx
<PlayAgainButton
  onClick={handlePlayAgain}
  disabled={!canRequestRematch()}
  pending={rematchRequestPending}
  visible={canRequestRematch() || rematchRequestPending}
/>
```

### RematchModal

```jsx
<RematchModal
  isOpen={showRematchModal}
  onAccept={handleAcceptRematch}
  onDecline={handleDeclineRematch}
  requestingPlayer={rematchRequestingPlayer}
/>
```

---

## State Management

### Frontend State Variables

```javascript
// Rematch-related state
const [rematchRequestPending, setRematchRequestPending] = useState(false);
const [showRematchModal, setShowRematchModal] = useState(false);
const [rematchRequestingPlayer, setRematchRequestingPlayer] = useState(null);
const [pendingRematchRequests, setPendingRematchRequests] = useState(new Set());
```

### Backend State Tracking

```python
# In game_rooms tracking
game_rooms[game_id] = {
    'players': set(),
    'spectators': set(),
    'room_name': str,
    'rematch_requests': set()  # Tracks who requested rematch
}
```

---

## Error Responses

### Common Error Messages

| Error                                     | Condition               |
| ----------------------------------------- | ----------------------- |
| `"Game not found"`                        | Invalid game_id         |
| `"Game is still in progress"`             | Rematch on active game  |
| `"Only game players can request rematch"` | Non-participant request |
| `"Rematch request already pending"`       | Duplicate request       |
| `"Failed to send rematch request"`        | Database/socket error   |

---

## Implementation Checklist

### Backend ✅

- [x] `rematch_request` handler
- [x] `rematch_accept` handler
- [x] `rematch_decline` handler
- [x] Game reset helper function
- [x] Disconnection cleanup
- [x] Duplicate request prevention
- [x] Error handling

### Frontend ✅

- [x] PlayAgainButton component
- [x] RematchModal component
- [x] Socket event listeners
- [x] State management
- [x] Toast notifications
- [x] Edge case handling
- [x] UI/UX integration

### Testing ✅

- [x] Happy path flow
- [x] Rejection handling
- [x] Simultaneous requests
- [x] Player disconnection
- [x] Error scenarios
- [x] UI state management
