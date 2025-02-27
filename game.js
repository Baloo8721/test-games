// Game configuration
const BOARD_SIZE = Math.min(window.innerWidth - 240, window.innerHeight - 40);
const SQUARE_SIZE = BOARD_SIZE / 8;

// Political figures data
const PIECES = {
    red: {
        king: { name: 'Donald Trump', portrait: 'trump1.jpg', meme: 'trump_meme1.jpg' },
        queen: { name: 'MTG', portrait: 'mtg.jpg', meme: 'mtg_meme.jpg' },
        rook: [
            { name: 'Vivek Ramaswamy', portrait: 'vivek.jpg', meme: 'vivek_meme.jpg' },
            { name: 'Ted Cruz', portrait: 'cruz.jpg', meme: 'cruz_meme.jpg' }
        ],
        knight: [
            { name: 'Elon Musk', portrait: 'elon.jpg', meme: 'elon_meme.jpg' },
            { name: 'Ron DeSantis', portrait: 'desantis.jpg', meme: 'desantis_meme.jpg' }
        ],
        bishop: [
            { name: 'Rand Paul', portrait: 'rand.jpg', meme: 'rand_meme.jpg' },
            { name: 'Mike Pence', portrait: 'pence.jpg', meme: 'pence_meme.jpg' }
        ],
        pawn: [
            { name: 'Matt Gaetz', portrait: 'gaetz.jpg', meme: 'gaetz_meme.jpg' },
            { name: 'RFK Jr', portrait: 'rfk.jpg', meme: 'rfk_meme.jpg' },
            { name: 'Marjorie T Greene', portrait: 'greene.jpg', meme: 'greene_meme.jpg' },
            { name: 'Josh Hawley', portrait: 'hawley.jpg', meme: 'hawley_meme.jpg' },
            { name: 'Jim Jordan', portrait: 'jordan.jpg', meme: 'jordan_meme.jpg' },
            { name: 'Lauren Boebert', portrait: 'boebert.jpg', meme: 'boebert_meme.jpg' },
            { name: 'Greg Abbott', portrait: 'abbott.jpg', meme: 'abbott_meme.jpg' },
            { name: 'Tim Scott', portrait: 'scott.jpg', meme: 'scott_meme.jpg' }
        ]
    },
    blue: {
        king: { name: 'Joe Biden', portrait: 'biden.jpg', meme: 'biden_meme.jpg' },
        queen: { name: 'Kamala Harris', portrait: 'harris.jpg', meme: 'harris_meme.jpg' },
        rook: [
            { name: 'Nancy Pelosi', portrait: 'pelosi.jpg', meme: 'pelosi_meme.jpg' },
            { name: 'Chuck Schumer', portrait: 'schumer.jpg', meme: 'schumer_meme.jpg' }
        ],
        knight: [
            { name: 'AOC', portrait: 'aoc.jpg', meme: 'aoc_meme.jpg' },
            { name: 'Bernie Sanders', portrait: 'bernie.jpg', meme: 'bernie_meme.jpg' }
        ],
        bishop: [
            { name: 'Elizabeth Warren', portrait: 'warren.jpg', meme: 'warren_meme.jpg' },
            { name: 'Pete Buttigieg', portrait: 'pete.jpg', meme: 'pete_meme.jpg' }
        ],
        pawn: [
            { name: 'Justin Trudeau', portrait: 'trudeau.jpg', meme: 'trudeau_meme.jpg' },
            { name: 'Gavin Newsom', portrait: 'newsom.jpg', meme: 'newsom_meme.jpg' },
            { name: 'Hillary Clinton', portrait: 'clinton.jpg', meme: 'clinton_meme.jpg' },
            { name: 'Maxine Waters', portrait: 'waters.jpg', meme: 'waters_meme.jpg' },
            { name: 'Ilhan Omar', portrait: 'omar.jpg', meme: 'omar_meme.jpg' },
            { name: 'John Fetterman', portrait: 'fetterman.jpg', meme: 'fetterman_meme.jpg' },
            { name: 'Gretchen Whitmer', portrait: 'whitmer.jpg', meme: 'whitmer_meme.jpg' },
            { name: 'Adam Schiff', portrait: 'schiff.jpg', meme: 'schiff_meme.jpg' }
        ]
    }
};

// Game state
let game = new Chess();
let board = null;
let selectedSquare = null;
let capturedPieces = { red: [], blue: [] };
let audioContext = null;
let backgroundMusic = null;
let isMuted = false;
let volume = 0.5;

// Initialize the game
function init() {
    const canvas = document.getElementById('chessBoard');
    canvas.width = BOARD_SIZE;
    canvas.height = BOARD_SIZE;

    // Initialize audio
    setupAudio();

    // Set up the board
    drawBoard();

    // Add event listeners
    canvas.addEventListener('click', handleClick);
    canvas.addEventListener('mousemove', handleMouseMove);

    // Set up audio controls
    document.getElementById('muteButton').addEventListener('click', toggleMute);
    document.getElementById('volumeSlider').addEventListener('input', handleVolumeChange);

    // Set up modals
    document.getElementById('continueButton').addEventListener('click', () => {
        document.getElementById('captureModal').classList.add('hidden');
    });

    document.getElementById('newGameButton').addEventListener('click', resetGame);
}

// Audio setup
function setupAudio() {
    try {
        audioContext = new (window.AudioContext || window.webkitAudioContext)();
        loadBackgroundMusic();
    } catch (e) {
        console.error('Web Audio API not supported:', e);
    }
}

async function loadBackgroundMusic() {
    try {
        const response = await fetch('audio/political_party_lofi.mp3');
        const arrayBuffer = await response.arrayBuffer();
        const audioBuffer = await audioContext.decodeAudioData(arrayBuffer);

        backgroundMusic = audioContext.createBufferSource();
        backgroundMusic.buffer = audioBuffer;
        backgroundMusic.loop = true;

        const gainNode = audioContext.createGain();
        gainNode.gain.value = volume;

        backgroundMusic.connect(gainNode);
        gainNode.connect(audioContext.destination);

        backgroundMusic.start();
    } catch (e) {
        console.error('Error loading background music:', e);
    }
}

// Draw functions
function drawBoard() {
    const ctx = document.getElementById('chessBoard').getContext('2d');

    // Draw squares
    for (let row = 0; row < 8; row++) {
        for (let col = 0; col < 8; col++) {
            const x = col * SQUARE_SIZE;
            const y = row * SQUARE_SIZE;
            ctx.fillStyle = (row + col) % 2 === 0 ? '#ffffff' : '#808080';
            ctx.fillRect(x, y, SQUARE_SIZE, SQUARE_SIZE);
        }
    }

    // Draw pieces
    const position = game.board();
    position.forEach((row, rowIndex) => {
        row.forEach((piece, colIndex) => {
            if (piece) {
                drawPiece(ctx, piece, colIndex, rowIndex);
            }
        });
    });

    // Draw selected square highlight
    if (selectedSquare) {
        const [col, row] = selectedSquare;
        ctx.strokeStyle = 'yellow';
        ctx.lineWidth = 3;
        ctx.strokeRect(
            col * SQUARE_SIZE,
            row * SQUARE_SIZE,
            SQUARE_SIZE,
            SQUARE_SIZE
        );

        // Draw valid moves
        const moves = game.moves({ square: selectedSquare, verbose: true });
        moves.forEach(move => {
            const [moveCol, moveRow] = [
                move.to.charCodeAt(0) - 'a'.charCodeAt(0),
                8 - parseInt(move.to[1])
            ];

            ctx.beginPath();
            ctx.arc(
                moveCol * SQUARE_SIZE + SQUARE_SIZE / 2,
                moveRow * SQUARE_SIZE + SQUARE_SIZE / 2,
                SQUARE_SIZE * 0.15,
                0,
                2 * Math.PI
            );
            ctx.fillStyle = 'rgba(0, 255, 0, 0.3)';
            ctx.fill();
            ctx.strokeStyle = 'rgba(0, 200, 0, 0.5)';
            ctx.stroke();
        });
    }
}

function drawPiece(ctx, piece, col, row) {
    const x = col * SQUARE_SIZE;
    const y = row * SQUARE_SIZE;
    const color = piece.color === 'w' ? 'red' : 'blue';
    const pieceType = getPieceType(piece);
    const pieceData = getPieceData(color, pieceType, col);

    // Load and draw portrait
    const img = new Image();
    img.src = `images/${pieceData.portrait}`;
    img.onload = () => {
        // Draw circular portrait
        ctx.save();
        ctx.beginPath();
        ctx.arc(
            x + SQUARE_SIZE / 2,
            y + SQUARE_SIZE * 0.4,
            SQUARE_SIZE * 0.35,
            0,
            2 * Math.PI
        );
        ctx.clip();
        ctx.drawImage(
            img,
            x + SQUARE_SIZE * 0.15,
            y + SQUARE_SIZE * 0.05,
            SQUARE_SIZE * 0.7,
            SQUARE_SIZE * 0.7
        );
        ctx.restore();

        // Draw name
        ctx.fillStyle = 'rgba(0, 0, 0, 0.7)';
        ctx.fillRect(
            x,
            y + SQUARE_SIZE * 0.75,
            SQUARE_SIZE,
            SQUARE_SIZE * 0.2
        );
        ctx.fillStyle = 'white';
        ctx.font = `${SQUARE_SIZE * 0.12}px Arial`;
        ctx.textAlign = 'center';
        ctx.fillText(
            pieceData.name,
            x + SQUARE_SIZE / 2,
            y + SQUARE_SIZE * 0.88
        );
    };
}

// Helper functions
function getPieceType(piece) {
    switch (piece.type) {
        case 'p': return 'pawn';
        case 'r': return 'rook';
        case 'n': return 'knight';
        case 'b': return 'bishop';
        case 'q': return 'queen';
        case 'k': return 'king';
    }
}

function getPieceData(color, type, col) {
    const pieces = PIECES[color][type];
    if (Array.isArray(pieces)) {
        // For pieces with multiple variants (rooks, knights, bishops, pawns)
        return pieces[col % pieces.length];
    }
    return pieces;
}

// Event handlers
function handleClick(event) {
    const rect = event.target.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;

    const col = Math.floor(x / SQUARE_SIZE);
    const row = Math.floor(y / SQUARE_SIZE);

    if (selectedSquare) {
        const [fromCol, fromRow] = selectedSquare;
        const from = `${String.fromCharCode(97 + fromCol)}${8 - fromRow}`;
        const to = `${String.fromCharCode(97 + col)}${8 - row}`;

        try {
            const move = game.move({
                from: from,
                to: to,
                promotion: 'q'
            });

            if (move) {
                if (move.captured) {
                    handleCapture(move);
                }

                if (game.game_over()) {
                    handleGameOver();
                }
            }
        } catch (e) {
            console.error('Invalid move:', e);
        }

        selectedSquare = null;
    } else {
        const piece = game.get(`${String.fromCharCode(97 + col)}${8 - row}`);
        if (piece && piece.color === (game.turn() === 'w' ? 'w' : 'b')) {
            selectedSquare = [col, row];
        }
    }

    drawBoard();
}

function handleMouseMove(event) {
    const rect = event.target.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;

    const col = Math.floor(x / SQUARE_SIZE);
    const row = Math.floor(y / SQUARE_SIZE);

    const piece = game.get(`${String.fromCharCode(97 + col)}${8 - row}`);
    if (piece) {
        const portrait = document.getElementById('piecePortrait');
        const color = piece.color === 'w' ? 'red' : 'blue';
        const pieceType = getPieceType(piece);
        const pieceData = getPieceData(color, pieceType, col);

        portrait.style.left = `${event.clientX + 10}px`;
        portrait.style.top = `${event.clientY + 10}px`;
        portrait.innerHTML = `<img src="images/${pieceData.portrait}" width="100">`;
        portrait.classList.remove('hidden');
    } else {
        document.getElementById('piecePortrait').classList.add('hidden');
    }
}

function handleCapture(move) {
    const capturedPiece = move.captured;
    const capturedColor = move.color === 'w' ? 'blue' : 'red';
    const pieceType = getPieceType({ type: capturedPiece });
    const pieceData = getPieceData(capturedColor, pieceType, move.to.charCodeAt(0) - 'a'.charCodeAt(0));

    capturedPieces[capturedColor].push(pieceData);
    updateCapturedPieces();

    // Show capture modal
    const modal = document.getElementById('captureModal');
    const memeImg = document.getElementById('memePicture');
    const pieceName = document.getElementById('capturedPieceName');

    memeImg.src = `images/${pieceData.meme}`;
    pieceName.textContent = pieceData.name;
    modal.classList.remove('hidden');
}

function handleGameOver() {
    const modal = document.getElementById('winnerModal');
    const text = document.getElementById('winnerText');
    const winner = game.turn() === 'w' ? 'DEMOCRATS' : 'REPUBLICANS';
    text.textContent = `${winner} WIN!`;
    modal.classList.remove('hidden');
}

function updateCapturedPieces() {
    ['red', 'blue'].forEach(color => {
        const list = document.getElementById(`captured${color.charAt(0).toUpperCase() + color.slice(1)}`);
        list.innerHTML = capturedPieces[color]
            .map(piece => `<div class="captured-piece">${piece.name}</div>`)
            .join('');
    });
}

// Audio controls
function toggleMute() {
    isMuted = !isMuted;
    if (backgroundMusic) {
        const gainNode = audioContext.createGain();
        gainNode.gain.value = isMuted ? 0 : volume;
        backgroundMusic.connect(gainNode);
        gainNode.connect(audioContext.destination);
    }
    document.getElementById('muteButton').textContent = isMuted ? '🔇' : '🔊';
}

function handleVolumeChange(event) {
    volume = event.target.value / 100;
    if (!isMuted && backgroundMusic) {
        const gainNode = audioContext.createGain();
        gainNode.gain.value = volume;
        backgroundMusic.connect(gainNode);
        gainNode.connect(audioContext.destination);
    }
}

function resetGame() {
    game = new Chess();
    selectedSquare = null;
    capturedPieces = { red: [], blue: [] };
    updateCapturedPieces();
    drawBoard();
    document.getElementById('winnerModal').classList.add('hidden');
}

// Start the game
init(); 