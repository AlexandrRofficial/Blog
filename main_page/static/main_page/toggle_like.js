document.addEventListener('DOMContentLoaded', function () {

    document.querySelectorAll('.like-form').forEach(form => {

        form.addEventListener('submit', function (e) {
            e.preventDefault();

            const url = form.dataset.url;
            const likesSpan = form.querySelector('.likes-count');
            const formData = new FormData(form);

            fetch(url, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': form.querySelector(
                        '[name=csrfmiddlewaretoken]'
                    ).value
                },
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                likesSpan.textContent = data.likes_count;
            });
        });

    });

});