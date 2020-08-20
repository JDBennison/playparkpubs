function sendMail(contactForm) {
    emailjs.send("gmail", "playparkpubs", {
        "from_name": contactForm.contact_name.value,
        "from_email": contactForm.contact_email.value,
        "website_message": contactForm.contact_message.value
    })
    .then(
        function(response) {
            console.log("SUCCESS", response);
        },
        function(error) {
            console.log("FAILED", error);
        }
    );
    return false;  // To block from loading a new page
}