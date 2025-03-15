function showMessageAndRedirect(message, redirectUrl) {
    alert(message);
    setTimeout(function () {
        window.location.href = redirectUrl;
    }, 2000);
}

document.addEventListener("DOMContentLoaded", function() {
    const successMessage = "Order created successfully.";
    const insufficientBalanceMessage = "Insufficient balance. Please recharge.";
    const orderCompletedMessage = "Order completed.";
    const refundProcessedMessage = "Refund processed successfully.";

    if (document.body.innerText.includes(successMessage)) {
        showMessageAndRedirect("Rental successful! Redirecting to order details...", window.location.href);
    }

    if (document.body.innerText.includes(insufficientBalanceMessage)) {
        showMessageAndRedirect("Insufficient balance. Redirecting to wallet recharge page...", "/wallet/");
    }

    if (document.body.innerText.includes(orderCompletedMessage)) {
        showMessageAndRedirect("Order completed! If a refund is due, it will be credited to your wallet.", "/wallet/");
    }

    if (document.body.innerText.includes(refundProcessedMessage)) {
        showMessageAndRedirect("Refund successfully processed. Redirecting to wallet...", "/wallet/");
    }
});