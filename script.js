// Sorting and filtering functionality
let allDramas = [];

// Load the dramas from our JSON file
fetch('dramas.json')
    .then(response => response.json())
    .then(dramas => {
        allDramas = dramas;
        // Sort alphabetically by default
        allDramas.sort((a, b) => (a.title || '').localeCompare(b.title || ''));
        displayDramas(allDramas);
        setupControls();
    })
    .catch(error => {
        console.error('Error loading dramas:', error);
        document.getElementById('drama-container').innerHTML = 
            '<p style="color: white; text-align: center;">Error loading dramas. Please try again.</p>';
    });

function displayDramas(dramas) {
    const container = document.getElementById('drama-container');
    container.innerHTML = ''; // Clear existing content
    
    // Update drama count
    document.getElementById('drama-count').textContent = dramas.length;
    
    dramas.forEach(drama => {
        const card = document.createElement('div');
        card.className = 'drama-card';
        
        const posterUrl = drama.poster || 'https://via.placeholder.com/250x350?text=No+Poster';
        const kdramaGroupBadge = drama.kdramaGroup && drama.kdramaGroup > 0 
            ? `<div class="kdrama-badge">${drama.kdramaGroup}</div>` 
            : '';
        const rating = drama.rating ? `⭐ ${drama.rating}/5` : 'Not rated';
        const genres = drama.genres && drama.genres.length > 0 
            ? drama.genres.map(g => `<span class="genre-tag">${g}</span>`).join('') 
            : '';
        
        const actors = drama.actors && drama.actors.length > 0
            ? `<strong>Actors:</strong> ${drama.actors.map(a => `<span class="actor-name" data-actor="${a}">${a}</span>`).join(', ')}`
            : '';
        const actresses = drama.actresses && drama.actresses.length > 0
            ? `<strong>Actresses:</strong> ${drama.actresses.map(a => `<span class="actor-name" data-actor="${a}">${a}</span>`).join(', ')}`
            : '';

        const plotSummary = drama.plotSummary 
            ? `<strong>Summary:</strong> ${drama.plotSummary}` 
            : '<strong>Summary:</strong> No summary available.';
        
        card.innerHTML = `
            <img src="${posterUrl}" alt="${drama.title}" class="drama-poster">
            ${kdramaGroupBadge}
            <div class="drama-info">
                <div class="drama-title">${drama.title}</div>
                <div class="drama-details">
                    <div class="rating">${rating}</div>
                    <div>${drama.year || 'Year unknown'}</div>
                    <div>${drama.country || ''}</div>
                    ${actors ? `<div>${actors}</div>` : ''}
                    ${actresses ? `<div>${actresses}</div>` : ''}
                    <div class="genres">${genres}</div>
                </div>
                <div class="expand-indicator">▼ Click for summary</div>
                <div class="plot-summary">${plotSummary}</div>
            </div>
        `;
        
        // Add click handler to toggle summary
        card.addEventListener('click', (e) => {
            // Don't toggle if clicking on actor name
            if (!e.target.classList.contains('actor-name')) {
                card.classList.toggle('expanded');
            }
        });

        // Add click handlers to actor names
        card.querySelectorAll('.actor-name').forEach(actorSpan => {
            actorSpan.addEventListener('click', (e) => {
                e.stopPropagation(); // Prevent card expansion
                const actorName = actorSpan.dataset.actor;
                showActorModal(actorName);
            });
        });

        container.appendChild(card);
    });
}

function setupControls() {
    const sortSelect = document.getElementById('sort-select');
    const filterSelect = document.getElementById('filter-select');
    const searchBox = document.getElementById('search-box');
    
    sortSelect.addEventListener('change', applyFiltersAndSort);
    filterSelect.addEventListener('change', applyFiltersAndSort);
    searchBox.addEventListener('input', (e) => {
        const searchText = e.target.value.toLowerCase();
        showAutocomplete(searchText);
        applyFiltersAndSort();
    });
}

function showAutocomplete(searchText) {
    const dropdown = document.getElementById('autocomplete-dropdown');
    
    if (!searchText || searchText.length < 2) {
        dropdown.classList.remove('show');
        dropdown.innerHTML = '';
        return;
    }
    
    // Collect all unique searchable terms
    const suggestions = new Set();
    
    allDramas.forEach(drama => {
        // Add title if it matches
        if (drama.title && drama.title.toLowerCase().includes(searchText)) {
            suggestions.add(drama.title);
        }
        
        // Add matching actors
        (drama.actors || []).forEach(actor => {
            if (actor.toLowerCase().includes(searchText)) {
                suggestions.add(actor);
            }
        });
        
        // Add matching actresses
        (drama.actresses || []).forEach(actress => {
            if (actress.toLowerCase().includes(searchText)) {
                suggestions.add(actress);
            }
        });
        
        // Add matching genres
        (drama.genres || []).forEach(genre => {
            if (genre.toLowerCase().includes(searchText)) {
                suggestions.add(genre);
            }
        });
    });
    
    // Convert to array and limit to 10 suggestions
    const suggestionArray = Array.from(suggestions).slice(0, 10);
    
    if (suggestionArray.length === 0) {
        dropdown.classList.remove('show');
        dropdown.innerHTML = '';
        return;
    }
    
    // Create dropdown items
    dropdown.innerHTML = suggestionArray
        .map(item => `<div class="autocomplete-item">${item}</div>`)
        .join('');
    
    dropdown.classList.add('show');
    
    // Add click handlers
    dropdown.querySelectorAll('.autocomplete-item').forEach(item => {
        item.addEventListener('click', () => {
            document.getElementById('search-box').value = item.textContent;
            dropdown.classList.remove('show');
            applyFiltersAndSort();
        });
    });
}
function applyFiltersAndSort() {
    let filteredDramas = [...allDramas];
    
    // Apply search
    const searchText = document.getElementById('search-box').value.toLowerCase();
    if (searchText) {
        filteredDramas = filteredDramas.filter(drama => {
            // Search in title, actors, actresses, genres, country
            const searchableText = [
                drama.title,
                ...(drama.actors || []),
                ...(drama.actresses || []),
                ...(drama.genres || []),
                drama.country
            ].join(' ').toLowerCase();
            
            return searchableText.includes(searchText);
        });
    }
    
    // Apply filter
    const filterValue = document.getElementById('filter-select').value;
    if (filterValue === 'rating-5') {
        filteredDramas = filteredDramas.filter(d => d.rating === 5);
    } else if (filterValue === 'rating-4') {
        filteredDramas = filteredDramas.filter(d => d.rating === 4);
    } else if (filterValue === 'rating-3') {
        filteredDramas = filteredDramas.filter(d => d.rating === 3);
    } else if (filterValue === 'rating-2') {
        filteredDramas = filteredDramas.filter(d => d.rating === 2);
    } else if (filterValue === 'rating-1') {
        filteredDramas = filteredDramas.filter(d => d.rating === 1);
    } else if (filterValue === 'kdrama-group') {
        filteredDramas = filteredDramas.filter(d => d.kdramaGroup && d.kdramaGroup > 0);
        // Sort by kdrama group number
        filteredDramas.sort((a, b) => Number(a.kdramaGroup || 999) - Number(b.kdramaGroup || 999));
        // Skip the sort dropdown and display immediately
        displayDramas(filteredDramas);
        return;
    }
    
    // Apply sort
    const sortValue = document.getElementById('sort-select').value;
    filteredDramas.sort((a, b) => {
        switch(sortValue) {
            case 'title-asc':
                return (a.title || '').localeCompare(b.title || '');
            case 'title-desc':
                return (b.title || '').localeCompare(a.title || '');
            case 'rating-desc':
                return (b.rating || 0) - (a.rating || 0);
            case 'rating-asc':
                return (a.rating || 0) - (b.rating || 0);
            case 'year-desc':
                return (b.year || 0) - (a.year || 0);
            case 'year-asc':
                return (a.year || 0) - (b.year || 0);
            case 'date-desc':
                return new Date(b.dateFinished || 0) - new Date(a.dateFinished || 0);
            case 'date-asc':
                return new Date(a.dateFinished || 0) - new Date(b.dateFinished || 0);
            default:
                return 0;
        }
    });
    
    // Clear and redisplay
    displayDramas(filteredDramas);
}
// Rating modal functionality
document.addEventListener('DOMContentLoaded', () => {
    const trigger = document.getElementById('rating-info-trigger');
    const modal = document.getElementById('rating-modal');
    const closeBtn = document.querySelector('.close-modal');

    if (trigger && modal) {
        trigger.addEventListener('click', () => {
            modal.classList.add('show');
        });

        closeBtn.addEventListener('click', () => {
            modal.classList.remove('show');
        });

        // Close when clicking outside the modal
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.classList.remove('show');
            }
        });
    }

    // Actor modal functionality
    const actorModal = document.getElementById('actor-modal');
    const closeActorBtn = document.querySelector('.close-actor-modal');

    if (actorModal && closeActorBtn) {
        closeActorBtn.addEventListener('click', () => {
            actorModal.classList.remove('show');
        });

        // Close when clicking outside the modal
        actorModal.addEventListener('click', (e) => {
            if (e.target === actorModal) {
                actorModal.classList.remove('show');
            }
        });
    }
});

// Function to show actor modal with dramas and stats
function showActorModal(actorName) {
    const modal = document.getElementById('actor-modal');
    const titleEl = document.getElementById('actor-modal-title');
    const statsEl = document.getElementById('actor-modal-stats');
    const dramasEl = document.getElementById('actor-modal-dramas');

    // Find all dramas featuring this actor
    const actorDramas = allDramas.filter(drama => {
        return (drama.actors && drama.actors.includes(actorName)) ||
               (drama.actresses && drama.actresses.includes(actorName));
    });

    // Find actor's profile image from first drama
    let profileImage = null;
    for (const drama of actorDramas) {
        if (drama.actors && drama.actors.includes(actorName)) {
            const actorIndex = drama.actors.indexOf(actorName);
            if (drama.actorImages && drama.actorImages[actorIndex]) {
                profileImage = drama.actorImages[actorIndex];
                break;
            }
        }
        if (drama.actresses && drama.actresses.includes(actorName)) {
            const actressIndex = drama.actresses.indexOf(actorName);
            if (drama.actressImages && drama.actressImages[actressIndex]) {
                profileImage = drama.actressImages[actressIndex];
                break;
            }
        }
    }

    // Calculate statistics
    const dramaCount = actorDramas.length;
    const ratedDramas = actorDramas.filter(d => d.rating && d.rating > 0);
    const avgRating = ratedDramas.length > 0
        ? (ratedDramas.reduce((sum, d) => sum + d.rating, 0) / ratedDramas.length).toFixed(1)
        : 'N/A';

    // Update modal content with profile image
    if (profileImage) {
        titleEl.innerHTML = `
            <img src="${profileImage}" alt="${actorName}" class="actor-profile-image">
            <span>${actorName}</span>
        `;
    } else {
        titleEl.textContent = actorName;
    }

    statsEl.innerHTML = `
        <p><strong>Dramas:</strong> ${dramaCount}</p>
        <p><strong>Average Drama Rating:</strong> ${avgRating !== 'N/A' ? `⭐ ${avgRating}/5` : 'Not rated'}</p>
    `;

    // Sort dramas by rating (highest first), then by title
    const sortedDramas = [...actorDramas].sort((a, b) => {
        if (b.rating !== a.rating) {
            return (b.rating || 0) - (a.rating || 0);
        }
        return (a.title || '').localeCompare(b.title || '');
    });

    // Create drama list
    dramasEl.innerHTML = sortedDramas.map(drama => {
        const rating = drama.rating ? `⭐ ${drama.rating}/5` : 'Not rated';
        const year = drama.year ? ` (${drama.year})` : '';
        return `
            <div class="actor-drama-item">
                <div class="actor-drama-title">${drama.title}${year}</div>
                <div class="actor-drama-rating">${rating}</div>
            </div>
        `;
    }).join('');

    // Show the modal
    modal.classList.add('show');
}