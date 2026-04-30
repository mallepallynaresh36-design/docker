function bookTicket() {
    let from = document.getElementById("from").value;
    let to = document.getElementById("to").value;
    let date = document.getElementById("date").value;
    let seats = document.getElementById("seats").value;

    if (!from || !to || !date || !seats) {
        document.getElementById("result").innerText = "⚠️ Please fill all fields";
        return;
    }

    document.getElementById("result").innerText =
        `✅ Ticket Booked from ${from} to ${to} on ${date} for ${seats} seat(s)`;
}
