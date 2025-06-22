# 🎮 NeoTicTac Rematch Feature - Test Guide

## Quick Test Scenarios

### 🚀 Basic Rematch Flow

1. **Start the Application**

   ```bash
   # Terminal 1 - Backend
   cd server && python run.py

   # Terminal 2 - Frontend
   cd client && npm run dev
   ```

2. **Create and Join Game**

   - Open browser to `http://localhost:5173`
   - Register/Login as Player 1
   - Create a new game
   - Open incognito window, register as Player 2
   - Join the game

3. **Complete a Game**

   - Play until win or draw
   - Notice "PLAY AGAIN" button appears for both players

4. **Test Rematch Request**
   - Player 1 clicks "PLAY AGAIN"
   - Player 2 sees modal: "{Player1} wants to play again!"
   - Player 2 clicks "Accept"
   - New game starts automatically
   - Toast shows "New game started!" 🚀

### ❌ Decline Scenario

1. Complete a game
2. Player 1 clicks "PLAY AGAIN"
3. Player 2 clicks "Decline"
4. Player 1 receives toast: "{Player2} declined the rematch" ❌
5. Button becomes available again

### ⚡ Simultaneous Request

1. Complete a game
2. Both players click "PLAY AGAIN" at the same time
3. No modal appears - new game starts immediately
4. Toast shows "New game started!" for both players

### 🔌 Disconnection Test

1. Player 1 sends rematch request
2. Player 2 disconnects (close browser/tab)
3. Player 1 receives: "{Player2} disconnected" 🔌
4. Modal state resets automatically

## 🔍 Visual Indicators

### Button States

- **Available**: Green neon glow, "🔁 PLAY AGAIN"
- **Pending**: Pulsing animation, "WAITING..."
- **Disabled**: Grayed out, no interaction

### Modal Features

- **Cyberpunk design** with neon green/pink colors
- **Non-dismissible** - must click Accept/Decline
- **Clear player identification**
- **Terminal-style footer**

### Toast Notifications

- **Request sent**: 📤 "Rematch request sent!"
- **New game**: 🚀 "New game started!"
- **Declined**: ❌ "{player} declined the rematch"
- **Disconnected**: 🔌 "{player} disconnected"

## 🛠️ Debug Console

Open browser DevTools and check Console/Network tabs for:

### Socket Events (Console)

```javascript
// Outgoing events
socket.emit('rematch_request', {...})
socket.emit('rematch_accept', {...})
socket.emit('rematch_decline', {...})

// Incoming events
socket.on('rematch_requested', {...})
socket.on('rematch_accepted', {...})
socket.on('rematch_declined', {...})
```

### Network Tab

- WebSocket connection status
- Socket.IO event messages
- Real-time message flow

## 🎯 Edge Cases to Test

1. **Rapid clicking** - Button should disable after first click
2. **Page refresh** - State should reset properly
3. **Multiple games** - Each game tracks requests independently
4. **Spectators** - Should see rematches but can't participate
5. **Game in progress** - Button only appears after completion

## ✅ Success Criteria

- [x] Button appears only when game is complete
- [x] Modal shows requesting player's name
- [x] Accept/decline work correctly
- [x] New game resets board and turn to X
- [x] Toast notifications work
- [x] Simultaneous requests handled
- [x] Disconnection cleanup works
- [x] No duplicate requests possible
- [x] UI matches cyberpunk theme
- [x] All animations smooth

## 🔧 Common Issues & Solutions

### Issue: Button doesn't appear

**Solution**: Check that game has `winner` or `is_draw = true`

### Issue: Modal doesn't show

**Solution**: Verify socket connection and event listeners

### Issue: Game doesn't reset

**Solution**: Check backend database commit and emit events

### Issue: Toast not showing

**Solution**: Ensure `react-hot-toast` is imported and configured

### Issue: Styling looks wrong

**Solution**: Check Tailwind CSS classes are compiled correctly

---

## 📱 Mobile Testing

The rematch feature is fully responsive:

- Modal adapts to screen size
- Touch-friendly button sizes
- Proper spacing on mobile
- Readable text at all sizes

## 🚀 Production Deployment

Before deploying:

1. Test all scenarios thoroughly
2. Check error handling
3. Verify database transactions
4. Test with multiple concurrent users
5. Monitor socket connection stability

---

**Happy Testing! 🎮✨**
