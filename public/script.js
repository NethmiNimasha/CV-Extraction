document.addEventListener('DOMContentLoaded', () => {
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('cv-upload');
    const uploadStatus = document.getElementById('upload-status');
    const profileContainer = document.getElementById('profile-container');
    const profileForm = document.getElementById('profile-form');
    const skillsContainer = document.getElementById('skills-container');
    const saveStatus = document.getElementById('save-status');

    let currentSkills = [];

    // --- Drag and Drop Handlers ---
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('drag-over');
    });

    dropZone.addEventListener('dragleave', (e) => {
        e.preventDefault();
        dropZone.classList.remove('drag-over');
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('drag-over');
        if (e.dataTransfer.files.length) {
            handleFileUpload(e.dataTransfer.files[0]);
        }
    });

    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length) {
            handleFileUpload(e.target.files[0]);
        }
    });

    // --- Core Logic ---
    async function handleFileUpload(file) {
        if (!['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'].includes(file.type)) {
            showStatus(uploadStatus, 'Invalid file type. Please upload PDF or DOCX.', 'error');
            return;
        }

        showStatus(uploadStatus, 'Extracting text...', '');
        
        try {
            // 1. Extract Text
            const formData = new FormData();
            formData.append('cv', file);
            
            const extractRes = await fetch('/extract', {
                method: 'POST',
                body: formData
            });
            
            if (!extractRes.ok) throw new Error('Failed to extract text from CV');
            const extractData = await extractRes.json();

            showStatus(uploadStatus, 'Parsing extracted data...', '');

            // 2. Parse Text via NLP API
            const parseRes = await fetch('/parse', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text: extractData.text })
            });

            if (!parseRes.ok) throw new Error('Failed to parse CV text');
            const parsedData = await parseRes.json();

            showStatus(uploadStatus, 'Success! Populating profile...', 'success');
            
            // 3. Populate UI
            setTimeout(() => {
                populateProfileUI(parsedData);
            }, 500);

        } catch (error) {
            showStatus(uploadStatus, error.message, 'error');
        }
    }

    function populateProfileUI(data) {
        // Hide upload, show profile
        document.querySelector('.upload-section').classList.add('hidden');
        profileContainer.classList.remove('hidden');

        // Populate fields
        document.getElementById('name').value = data.name || '';
        document.getElementById('email').value = data.email || '';
        document.getElementById('education').value = (data.education || []).join('\n');
        document.getElementById('experience').value = (data.experience || []).join('\n');

        // Populate skills
        currentSkills = data.skills || [];
        renderSkills();
    }

    function renderSkills() {
        skillsContainer.innerHTML = '';
        currentSkills.forEach((skill, index) => {
            const tag = document.createElement('span');
            tag.className = 'tag';
            tag.innerHTML = `${skill} <span class="remove-tag" data-index="${index}">&times;</span>`;
            skillsContainer.appendChild(tag);
        });

        // Update hidden input
        document.getElementById('skills').value = JSON.stringify(currentSkills);
    }

    skillsContainer.addEventListener('click', (e) => {
        if (e.target.classList.contains('remove-tag')) {
            const index = e.target.getAttribute('data-index');
            currentSkills.splice(index, 1);
            renderSkills();
        }
    });

    document.getElementById('btn-cancel').addEventListener('click', () => {
        profileContainer.classList.add('hidden');
        document.querySelector('.upload-section').classList.remove('hidden');
        uploadStatus.innerText = '';
        fileInput.value = '';
    });

    profileForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        saveStatus.innerText = 'Saving...';
        saveStatus.className = 'status-message';

        const profileData = {
            name: document.getElementById('name').value,
            email: document.getElementById('email').value,
            skills: currentSkills,
            education: document.getElementById('education').value.split('\n').filter(s=>s.trim()),
            experience: document.getElementById('experience').value.split('\n').filter(s=>s.trim())
        };

        try {
            const res = await fetch('/profile', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(profileData)
            });

            if (!res.ok) throw new Error('Failed to save profile');
            
            showStatus(saveStatus, 'Profile saved successfully!', 'success');
        } catch (error) {
            showStatus(saveStatus, error.message, 'error');
        }
    });

    function showStatus(element, message, type) {
        element.innerText = message;
        element.className = `status-message ${type}`;
    }
});
