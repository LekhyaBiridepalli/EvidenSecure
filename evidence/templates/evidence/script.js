document.addEventListener('DOMContentLoaded', () => {
    // Sample data for demonstration
    const cases = [
        { id: 'C001', name: 'Case 1', status: 'Open', investigator: 'John Doe' },
        { id: 'C002', name: 'Case 2', status: 'Pending', investigator: 'Jane Smith' },
    ];

    const evidence = [
        { id: 'E001', caseId: 'C001', status: 'Under Review' },
        { id: 'E002', caseId: 'C002', status: 'Accepted' },
    ];

    const users = [
        { id: 'U001', name: 'Admin User', role: 'Admin', status: 'Active' },
        { id: 'U002', name: 'Investigator', role: 'Investigator', status: 'Active' },
    ];

    const logs = [
        { timestamp: '2023-10-01 10:00', user: 'Admin User', action: 'Logged in' },
        { timestamp: '2023-10-01 10:05', user: 'Investigator', action: 'Updated Case C001' },
    ];

    // Populate case list
    const caseList = document.getElementById('case-list');
    cases.forEach(caseItem => {
        const row = `<tr>
            <td>${caseItem.id}</td>
            <td>${caseItem.name}</td>
            <td>${caseItem.status}</td>
            <td>${caseItem.investigator}</td>
        </tr>`;
        caseList.innerHTML += row;
    });

    // Populate evidence list
    const evidenceList = document.getElementById('evidence-list');
    evidence.forEach(evidenceItem => {
        const row = `<tr>
            <td>${evidenceItem.id}</td>
            <td>${evidenceItem.caseId}</td>
            <td >${evidenceItem.status}</td>
        </tr>`;
        evidenceList.innerHTML += row;
    });

    // Populate user list
    const userList = document.getElementById('user-list');
    users.forEach(user => {
        const row = `<tr>
            <td>${user.id}</td>
            <td>${user.name}</td>
            <td>${user.role}</td>
            <td>${user.status}</td>
        </tr>`;
        userList.innerHTML += row;
    });

    // Populate log list
    const logList = document.getElementById('log-list');
    logs.forEach(log => {
        const row = `<tr>
            <td>${log.timestamp}</td>
            <td>${log.user}</td>
            <td>${log.action}</td>
        </tr>`;
        logList.innerHTML += row;
    });

    // Update stats
    document.getElementById('total-cases').innerText = cases.length;
    document.getElementById('open-cases').innerText = cases.filter(c => c.status === 'Open').length;
    document.getElementById('pending-evidence').innerText = evidence.filter(e => e.status === 'Under Review').length;
    document.getElementById('closed-cases').innerText = cases.filter(c => c.status === 'Closed').length;
}); 