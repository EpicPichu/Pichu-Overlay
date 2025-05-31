const version = '0.9'
let apiCache = {};
let sorting = 1;
let direction = false;



const colorOrder = {
    'rgb(255, 255, 255)': 1,
    'rgb(170, 0, 0)': 2,
    'rgb(255, 170, 0)': 3,
    'rgb(85, 255, 255)': 4,
    'rgb(85, 255, 85)': 5,
    'rgb(170, 170, 170)': 6
};

function togglesorting(columnIndex) {
    sorting = columnIndex;
    const table = document.getElementById("main-table");
    const th = table.querySelectorAll("th")[sorting];

    // Get the sort direction: ascending or descending
    if (!th.classList.contains("sorted-asc") && !th.classList.contains("sorted-desc")) {
        isAscending = false; // First click: descending
    } else if (th.classList.contains("sorted-desc")) {
        isAscending = true; // Toggle to ascending
    } else {
        isAscending = false; // Toggle back to descending
    }
    // Reset all header sort classes
    table.querySelectorAll("th").forEach(th => th.classList.remove("sorted-asc", "sorted-desc"));

    // Set the new sort direction class
    th.classList.add(isAscending ? "sorted-asc" : "sorted-desc");

    direction = isAscending;
    sortable();
}

function sortable() {
    const table = document.getElementById("main-table");
    const tbody = table.tBodies[0];
    const rows = Array.from(tbody.rows);


    rows.sort((a, b) => {
        let cellA = a.cells[sorting].textContent.trim();
        let cellB = b.cells[sorting].textContent.trim();

        if (sorting === 1) {
            cellA = cellA.slice(1, -1);
            cellB = cellB.slice(1, -1);
        }

        // Handle numeric sorting
        const numA = parseFloat(cellA);
        const numB = parseFloat(cellB);

        // If both cells are numeric, sort them numerically
        if (!isNaN(numA) && !isNaN(numB)) {
            return direction
                ? numA - numB  // Ascending
                : numB - numA; // Descending
        }

        // If they are not numeric, handle text color sorting (for text-based columns)
        const colorA = window.getComputedStyle(a.cells[sorting]).color;
        const colorB = window.getComputedStyle(b.cells[sorting]).color;

        const colorNameA = colorOrder[colorA];
        const colorNameB = colorOrder[colorB];

        // If they are not numeric, compare based on the defined color order
        return direction
            ? colorNameA - colorNameB  // Ascending order by color
            : colorNameB - colorNameA; // Descending order by color
    });

    // Reattach sorted rows
    rows.forEach(row => tbody.appendChild(row));
}

class StatsFetcher {
    constructor(username, interval = 'lifetime', gamemode = 'all_modes') {
        this.username = username;
        this.interval = interval;
        this.gamemode = gamemode;
        this.colors = ['lightgray', 'lightcyan', 'lightblue', 'lightgreen', 'lightsalmon', 'lightcoral'];
        this.rankNames = ['VIP', 'Elite', 'Titan', 'Champion', 'YouTube']
        this.rankColors = {
            'VIP': [85, 255, 85],
            'Elite': [85, 255, 255],
            'Titan': [255, 170, 0],
            'Champion': [170, 0, 0],
            'YouTube': [255, 120, 120]
        };
    }

    mapValue(x, inMin, inMax, outMin, outMax) {
        if (x > inMax) return outMax;
        return Math.round((x - inMin) * (outMax - outMin) / (inMax - inMin) + outMin);
    }

    getLevelColor(level) {
        if (level < 5) return 'gray';
        if (level < 10 || (level >= 40 && level < 45)) return 'lime';
        if (level < 15 || (level >= 45 && level < 50)) return 'aqua';
        if (level < 20 || (level >= 50 && level < 60)) return 'pink';
        if (level < 25 || (level >= 60 && level < 75)) return 'orange';
        if (level < 30 || (level >= 75 && level < 100)) return 'yellow';
        if (level < 35 || level >= 100) return 'red';
        return 'white';
    }

    calculateRatio(n1 = 0, n2 = 0) {
        let out = n1 !== 0 ? (n2 !== 0 ? n1 / n2 : n1) : 0;
        let rounded = Math.round(out * 100) / 100;
        let ratio = rounded < 10 ? rounded.toFixed(2) : rounded < 100 ? rounded.toFixed(1) : String(Math.floor(rounded));
        let color = ratio < 1 ? 'red' : ratio > 1 ? 'lime' : 'white';

        return [ratio, color];
    }

    getRank(ranks) {
        const gameRanks = ranks.filter(rank => rank.name.startsWith("games"));

        if (gameRanks.length === 0) return null;

        // Sort by rank priority (highest first)
        gameRanks.sort((a, b) =>
            this.rankNames.indexOf(b.displayName) - this.rankNames.indexOf(a.displayName)
        );

        return gameRanks[0].displayName; // Return the highest rank
    }

    async fetchStats() {
        try {

            if (apiCache[this.username]) {
                return apiCache[this.username];
            }

            const profileResponse = fetch(`https://stats.pika-network.net/api/profile/${this.username}`);
            const statsResponse = fetch(`https://stats.pika-network.net/api/profile/${this.username}/leaderboard?type=BEDWARS&interval=${this.interval}&mode=${this.gamemode}`);
            
            const [profile, stats] = await Promise.all([profileResponse, statsResponse]);
            
            if (![200, 429].includes(profile.status)) {
                apiCache[this.username] = this.username;
                return [this.username];
            }   if (profile.status == 429) return [this.username];

            const profileData = await profile.json();

            if (!profileData.rank) {
                apiCache[this.username] = this.username;
                return [this.username];
            }

            const level = profileData.rank.level;
            const levelColor = this.getLevelColor(level);
            
            const rank = this.getRank(profileData.ranks)
            const rankColor = this.rankColors[rank] || [170, 170, 170];

            const guild = profileData.clan ? profileData.clan.tag : '-';
            

            if (![200, 429].includes(stats.status)) {
                parsedStats = [this.username, level, levelColor, rankColor, guild];
                apiCache[this.username] = parsedStats;
                return parsedStats;
            }   if (stats.status == 429) return [this.username, level, levelColor, rankColor, guild];

            const statsData = await stats.json();

            const getStat = (key) => (statsData[key] && statsData[key].entries != null) ? parseInt(statsData[key].entries[0].value) : 0;

            const wins = getStat('Wins');
            const winsColor = this.colors[this.mapValue(wins, 0, 2000, 0, 5)]
            const losses = getStat('Losses');
            const wlr = this.calculateRatio(wins, losses);

            const fkills = getStat('Final kills');
            const fkillsColor = this.colors[this.mapValue(fkills, 0, 4000, 0, 5)]
            const fdeaths = getStat('Final deaths');
            const fkdr = this.calculateRatio(fkills, fdeaths);

            const kills = getStat('Kills');
            const killsColor = this.colors[this.mapValue(kills, 0, 10000, 0, 5)]
            const deaths = getStat('Deaths');
            const kdr = this.calculateRatio(kills, deaths);

            const winstreak = getStat('Highest winstreak reached');
            const winstreakColor = this.mapValue(winstreak, 0, 360, 0, 5);

            let parsedStats = [
                this.username, level, levelColor, rankColor, guild,
                wins, winsColor, wlr,
                fkills, fkillsColor, fkdr,
                kills, killsColor, kdr,
                winstreak, winstreakColor
            ]

            apiCache[this.username] = parsedStats;

            return parsedStats;

        } catch (error) {
            console.error('Error fetching stats:', error);
            return null;
        }
    }
}

async function asyncfetcher(usernames) {
    const fetchers = usernames.map(username => new StatsFetcher(username).fetchStats());
    const results = await Promise.all(fetchers);
    return results
}

function parseUsers(usernames = []) {
    const rows = document.querySelectorAll('tbody tr');
    const titles = new Set;

    rows.forEach(row => {
        if (row.title) {
            titles.add(row.title);
        }
    });

    return Array.from(new Set([...usernames].filter(item => !titles.has(item))));
}


function rowfetcher(username, level = '0', levelColor = 'white', rankColor = 'white', guild = 'NICKED',
    wins = '-', winsColor = 'white', wlr = '-',
    fkills = '-', fkillsColor = 'white', fkdr = '-',
    kills = '-', killsColor = 'white', kdr = '-',
    winstreak = '-', winstreakColor = 'white') {

    let html_string = `
    <tr title="${username}">
    <td id="heads"><img src="https://mc-heads.net/avatar/${username}/8"></td>
    <td style="color: ${levelColor}">[${level}]</td>
    <td style="color: rgb(${rankColor[0]}, ${rankColor[1]}, ${rankColor[2]}); text-align: left;">${username}</td>
    <td style="color: ${winsColor}">${wins}</td>
    <td style="color: ${wlr[1]}">${wlr[0]}</td>
    <td style="color: ${fkillsColor}">${fkills}</td>
    <td style="color: ${fkdr[1]}">${fkdr[0]}</td>
    <td style="color: ${killsColor}">${kills}</td>
    <td style="color: ${kdr[1]}">${kdr[0]}</td>
    <td style="color: ${winstreakColor}">${winstreak}</td>
    <td style="color: white">[${guild}]</td>
    </tr>
    `

    return html_string;
}

function rowAppend(rows) {
    const table = document.getElementById("main-table");
    if (table) {
        // Find or create tbody inside the table
        let tbody = table.querySelector("tbody");

        // If no tbody exists, create one
        if (!tbody) {
            tbody = document.createElement("tbody");
            table.appendChild(tbody);
        }

        // Append the rows (ensure `rows` contains <tr> elements)
        tbody.insertAdjacentHTML("beforeend", rows);
    } else {
        console.error("Table with ID 'main-table' not found!");
    }
}

function rowRemove(title) {
    const table = document.getElementById('main-table'); // Get the table by ID
    if (!table) {
        console.error('Table with ID "main-table" not found!');
        return;
    }

    const rows = table.querySelectorAll('tbody tr'); // Get all rows inside tbody
    rows.forEach(row => {
        const cells = row.getElementsByTagName('td'); // Get all <td> cells in the row
        for (let cell of cells) {
            if (cell.textContent.trim() === title) { // Check if the cell text matches the title
                row.remove(); // Remove the row
                return; // Exit after deleting the first matching row
            }
        }
    });
}

function rowClear() {
    const table = document.getElementById('main-table'); // Get the table by its ID
    if (table) {
        const tbody = table.querySelector('tbody'); // Get the tbody inside the table (optional, depends on your table structure)

        if (tbody) {
            // Remove all <tr> elements inside the tbody
            while (tbody.rows.length > 0) {
                tbody.deleteRow(0); // Delete the first row repeatedly until there are no rows left
            }
        } else {
            // If there is no tbody, remove rows from the entire table
            while (table.rows.length > 0) {
                table.deleteRow(0);
            }
        }
    } else {
        console.error('Table with ID "main-table" not found!');
    }

    document.getElementById('title').textContent = "Pichu Overlay (0)"
    document.getElementById('playercount').textContent = "(0)"
}

function openConfig() {
    const modal = document.getElementById("config-flex");
    modal.style.display = "flex";
    setTimeout(() => {
        modal.style.opacity = "100%";
    }, 1);
}

function closeConfig() {
    const modal = document.getElementById("config-flex");
    modal.style.opacity = "0%";
    setTimeout(() => {
        modal.style.display = "none";
    }, 100);
}

var socket = new WebSocket('ws://127.0.0.1:6969/ws');

socket.onopen = function () {
    console.log('Connected to WebSocket');
    socket.send('VERSION: '+version)
    document.getElementById('status').textContent = '(Connected)'
    document.getElementById('status').style.color = 'lime'
};

socket.onclose = function () {
    console.log('WebSocket connection closed');
    document.getElementById('status').textContent = '(Connection lost)'
    document.getElementById('status').style.color = 'red'
};

socket.onerror = function (error) {
    console.error('WebSocket Error: ', error);
    document.getElementById('status').textContent = '(Connection error)'
    document.getElementById('status').style.color = 'red'
};

socket.onmessage = async function (event) {
    console.log('Received message: ' + event.data);

    if (event.data.startsWith('TAB: ')) {
        rowClear()

        let string = event.data.substring(5);
        let usernames = parseUsers(string.split(', '));

        document.getElementById('playercount').textContent = `(${usernames.length})`
        document.getElementById('title').textContent = `Pichu Overlay (${usernames.length})`
        let stats = await asyncfetcher(usernames);
        stats.forEach(stats => {
            rowAppend(rowfetcher(...stats));
        });

        sortable(sorting);
    };

    if (event.data.startsWith("JOIN: ")) {
        let username = parseUsers([event.data.substring(6)]);
        let stats = await asyncfetcher(username);
        stats.forEach(stats => {
            rowAppend(rowfetcher(...stats));
        });
        sortable(sorting);
    }

    if (event.data.startsWith("LEAVE: ")) {
        let username = event.data.substring(7);
        rowRemove(username);
        sortable(sorting);
    }

    if (event.data.startsWith("PLAYERCOUNT: ")) {
        let playercount = event.data.substring(13);
        document.getElementById('playercount').textContent = playercount
        document.getElementById('title').textContent = "Pichu Overlay " + playercount
    }

    if (event.data.startsWith('CLIENT: ')) {
        let client = event.data.substring(8);

        const clientColors = {
            'Lunar Client': 'lightskyblue',
            'Badlion Client': 'lightgoldenrodyellow',
            'Vanilla': 'lightgreen',
            'Custom': 'orange'
        };

        const clientIcons = {
            'Lunar Client': 'assets/lunar.png',
            'Badlion Client': 'assets/badlion.png',
            'Vanilla': 'assets/minecraft.png',
            'Custom': 'assets/minecraft.png'
        }


        document.getElementById('clientname').textContent = client;
        document.getElementById('clientname').style.color = clientColors[client];

        document.getElementById('clienticon').setAttribute('src', clientIcons[client])
    }

    if (event.data.startsWith('LOG_PATH: ')) {
        let path = event.data.substring(10);
        document.getElementById('logpath-input').value = path
    }

    if (event.data === "OUTDATED_VER") {
        document.getElementById('status').textContent = '(Connected (Outdated server)'
        document.getElementById('status').style.color = 'green'
    }
};


function selectLog() {
    socket.send('CLIENT_CHANGE: Custom');
}

document.addEventListener('DOMContentLoaded', function() {
document.querySelectorAll('input[name="choice"]').forEach((radio) => {
    radio.addEventListener("change", (event) => {
        console.log("CLIENT_CHANGE: ", event.target.value);
        socket.send("CLIENT_CHANGE: "+ event.target.value);
    });
  });
});
