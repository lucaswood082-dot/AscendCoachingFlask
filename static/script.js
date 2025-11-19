// small friendly behavior: confirm before leaving signup
document.addEventListener('DOMContentLoaded', function(){
    const forms = document.querySelectorAll('.form-box');
    forms.forEach(f => {
        f.addEventListener('submit', function(){
            // little client-side check (could be expanded)
            // we won't block submit — but you could confirm
            // console.log('form submitted');
        });
    });
});
