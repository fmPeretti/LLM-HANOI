let gameData = null;
let currentMoveIndex = -1;
let isPlaying = false;
let playInterval = null;
let isAnimating = false;

// Initialize the game
document.addEventListener('DOMContentLoaded', function() {
    // Set up event listeners
    document.getElementById('discCount').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            solvePuzzle();
        }
    });
});

async function solvePuzzle() {
    const discCount = parseInt(document.getElementById('discCount').value);
    
    if (discCount < 1 || discCount > 10) {
        showError('Please enter a number between 1 and 10');
        return;
    }

    showLoading(true);
    hideError();
    
    try {
        const response = await fetch('/solve', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ discs: discCount })
        });

        const data = await response.json();
        
        if (data.success) {
            gameData = data;
            currentMoveIndex = -1;
            setupGame();
        } else {
            showError(data.error || 'Failed to solve puzzle');
        }
    } catch (error) {
        showError('Error connecting to server: ' + error.message);
    } finally {
        showLoading(false);
    }
}

function setupGame() {
    // Show game sections
    document.getElementById('infoSection').style.display = 'block';
    document.getElementById('gameSection').style.display = 'block';
    document.getElementById('moveInfo').style.display = 'block';
    document.getElementById('controls').style.display = 'block';
    
    // Hide completion message
    document.getElementById('completionMessage').style.display = 'none';
    
    // Update stats
    document.getElementById('currentMove').textContent = '0';
    document.getElementById('totalMoves').textContent = gameData.total_moves;
    document.getElementById('optimalMoves').textContent = gameData.minimum_moves;
    
    // Initialize towers with initial state
    updateTowers(gameData.initial_state);
    
    // Update move description
    document.getElementById('moveDescription').textContent = 
        `Ready to solve with ${gameData.moves[0].towers.A.length + 1} discs. Click "Play" or "Next" to start!`;
    
    // Reset controls
    document.getElementById('prevBtn').disabled = true;
    document.getElementById('nextBtn').disabled = false;
    document.getElementById('playPauseBtn').innerHTML = '▶️ Play';
    isPlaying = false;
    
    if (playInterval) {
        clearInterval(playInterval);
        playInterval = null;
    }
}

function updateTowers(towersState) {
    const towers = ['A', 'B', 'C'];
    
    towers.forEach(tower => {
        const container = document.getElementById(`discs${tower}`);
        container.innerHTML = '';
        
        towersState[tower].forEach(discSize => {
            const disc = document.createElement('div');
            disc.className = `disc disc-${discSize}`;
            disc.textContent = discSize;
            container.appendChild(disc);
        });
    });
}

function nextMove() {
    if (currentMoveIndex >= gameData.moves.length - 1 || isAnimating) return;
    
    currentMoveIndex++;
    const move = gameData.moves[currentMoveIndex];
    
    // Update move counter
    document.getElementById('currentMove').textContent = move.move_number;
    
    // Update move description
    document.getElementById('moveDescription').textContent = 
        `Move ${move.move_number}: Move disc ${move.disc} from Tower ${move.from} to Tower ${move.to}`;
    
    // Animate the move
    animateMove(move, () => {
        // Update towers after animation
        updateTowers(move.towers);
        
        // Update button states
        document.getElementById('prevBtn').disabled = currentMoveIndex <= 0;
        document.getElementById('nextBtn').disabled = currentMoveIndex >= gameData.moves.length - 1;
        
        // Check if puzzle is completed
        if (currentMoveIndex >= gameData.moves.length - 1) {
            showCompletion();
        }
    });
}

function previousMove() {
    if (currentMoveIndex <= 0 || isAnimating) return;
    
    currentMoveIndex--;
    
    if (currentMoveIndex < 0) {
        // Back to initial state
        updateTowers(gameData.initial_state);
        document.getElementById('currentMove').textContent = '0';
        document.getElementById('moveDescription').textContent = 
            `Ready to solve with ${gameData.moves[0].towers.A.length} discs. Click "Play" or "Next" to start!`;
    } else {
        const move = gameData.moves[currentMoveIndex];
        updateTowers(move.towers);
        document.getElementById('currentMove').textContent = move.move_number;
        document.getElementById('moveDescription').textContent = 
            `Move ${move.move_number}: Move disc ${move.disc} from Tower ${move.from} to Tower ${move.to}`;
    }
    
    // Update button states
    document.getElementById('prevBtn').disabled = currentMoveIndex <= 0;
    document.getElementById('nextBtn').disabled = currentMoveIndex >= gameData.moves.length - 1;
    
    // Hide completion message if going back
    document.getElementById('completionMessage').style.display = 'none';
}

function animateMove(move, callback) {
    isAnimating = true;
    
    // Find the disc element to animate
    const sourceContainer = document.getElementById(`discs${move.from}`);
    const targetContainer = document.getElementById(`discs${move.to}`);
    
    if (sourceContainer.children.length > 0) {
        const discElement = sourceContainer.children[sourceContainer.children.length - 1];
        discElement.classList.add('moving');
        
        setTimeout(() => {
            discElement.classList.remove('moving');
            isAnimating = false;
            if (callback) callback();
        }, 800);
    } else {
        isAnimating = false;
        if (callback) callback();
    }
}

function togglePlayPause() {
    if (isPlaying) {
        // Pause
        isPlaying = false;
        document.getElementById('playPauseBtn').innerHTML = '▶️ Play';
        if (playInterval) {
            clearInterval(playInterval);
            playInterval = null;
        }
    } else {
        // Play
        if (currentMoveIndex >= gameData.moves.length - 1) {
            // Reset to beginning if at end
            resetPuzzle();
        }
        
        isPlaying = true;
        document.getElementById('playPauseBtn').innerHTML = '⏸️ Pause';
        
        playInterval = setInterval(() => {
            if (!isAnimating) {
                nextMove();
                if (currentMoveIndex >= gameData.moves.length - 1) {
                    // Stop playing when completed
                    togglePlayPause();
                }
            }
        }, 1000);
    }
}

function resetPuzzle() {
    // Stop playing
    if (isPlaying) {
        togglePlayPause();
    }
    
    // Reset to initial state
    currentMoveIndex = -1;
    updateTowers(gameData.initial_state);
    document.getElementById('currentMove').textContent = '0';
    document.getElementById('moveDescription').textContent = 
        `Ready to solve with ${gameData.moves[0].towers.A.length} discs. Click "Play" or "Next" to start!`;
    
    // Update button states
    document.getElementById('prevBtn').disabled = true;
    document.getElementById('nextBtn').disabled = false;
    
    // Hide completion message
    document.getElementById('completionMessage').style.display = 'none';
}

function showCompletion() {
    document.getElementById('finalMoveCount').textContent = gameData.total_moves;
    document.getElementById('completionMessage').style.display = 'block';
    
    // Stop playing
    if (isPlaying) {
        togglePlayPause();
    }
}

function showLoading(show) {
    document.getElementById('loading').style.display = show ? 'block' : 'none';
}

function showError(message) {
    const errorDiv = document.getElementById('errorMessage');
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';
    
    // Hide error after 5 seconds
    setTimeout(() => {
        hideError();
    }, 5000);
}

function hideError() {
    document.getElementById('errorMessage').style.display = 'none';
}

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    if (!gameData) return;
    
    switch(e.key) {
        case 'ArrowLeft':
            e.preventDefault();
            previousMove();
            break;
        case 'ArrowRight':
            e.preventDefault();
            nextMove();
            break;
        case ' ':
            e.preventDefault();
            togglePlayPause();
            break;
        case 'r':
            e.preventDefault();
            resetPuzzle();
            break;
    }
}); 