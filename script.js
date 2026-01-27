// Load the dramas from our JSON file
fetch('dramas.json')
    .then(response => response.json())
    .then(dramas => {
        displayDramas(dramas);
    })
    .catch(error => {
        console.error('Error loading dramas:', error);
        document.getElementById('drama-container').innerHTML = 
            '<p style="color: white; text-align: center;">Error loading dramas. Please try again.</p>';
    });

function displayDramas(dramas) {
    const container = document.getElementById('drama-container');
    
    dramas.forEach(drama => {
        const card = document.createElement('div');
        card.className = 'drama-card';
        
        const posterUrl = drama.poster || 'https://via.placeholder.com/250x350?text=No+Poster';
        const rating = drama.rating ? `⭐ ${drama.rating}/5` : 'Not rated';
        const genres = drama.genres && drama.genres.length > 0 
            ? drama.genres.map(g => `<span class="genre-tag">${g}</span>`).join('') 
            : '';
        
        card.innerHTML = `
            <img src="${posterUrl}" alt="${drama.title}" class="drama-poster">
            <div class="drama-info">
                <div class="drama-title">${drama.title}</div>
                <div class="drama-details">
                    <div class="rating">${rating}</div>
                    <div>${drama.year || 'Year unknown'}</div>
                    <div>${drama.country || ''}</div>
                    <div class="genres">${genres}</div>
                </div>
            </div>
        `;
        
        container.appendChild(card);
    });
}