$(document).ready(function () {
    function showMessage(message, type) {
        $("#message")
            .text(message)
            .attr("class", "message " + type)
            .show();
        setTimeout(() => {
            $("#message").hide();
        }, 3000);
    }

    function loadBooks() {
        $.ajax({
            url: "/books",
            method: "GET",
            success: function (data) {
                let rows = "";
                data.forEach((book) => {
                    rows += `
                        <tr>
                            <td>${book.title}</td>
                            <td>${book.author}</td>
                            <td>${book.published_date}</td>
                            <td>${book.isbn}</td>
                            <td>${book.pages}</td>
                            <td>
                                <button class="edit-button" data-id="${book.id}">Edit</button>
                                <button class="delete-button" data-id="${book.id}">Delete</button>
                            </td>
                        </tr>
                    `;
                });
                $("#books-tbody").html(rows);
            },
            error: function (xhr) {
                showMessage(`Failed to load books: ${xhr.responseText}`, "error");
            },
        });
    }

    function clearForm() {
        $("#book-id").val("");
        $("#title").val("");
        $("#author").val("");
        $("#published_date").val("");
        $("#isbn").val("");
        $("#pages").val("");
    }

    $("#add-book-button").click(function () {
        clearForm();
        $("#form-title").text("Add Book");
        $("#submit-button").text("Add Book");
        $("#book-form").show();
    });

    $("#cancel-button").click(function () {
        $("#book-form").hide();
    });

    $(document).on("click", ".edit-button", function () {
        const id = $(this).data("id");
        $.ajax({
            url: `/books/${id}`,
            method: "GET",
            success: function (book) {
                $("#book-id").val(book.id);
                $("#title").val(book.title);
                $("#author").val(book.author);
                $("#published_date").val(book.published_date);
                $("#isbn").val(book.isbn);
                $("#pages").val(book.pages);
                $("#form-title").text("Edit Book");
                $("#submit-button").text("Update Book");
                $("#book-form").show();
            },
            error: function (xhr) {
                showMessage(`Failed to load book details: ${xhr.responseText}`, "error");
            },
        });
    });

    $(document).on("click", ".delete-button", function () {
        const id = $(this).data("id");
        if (confirm("Are you sure you want to delete this book?")) {
            $.ajax({
                url: `/books/${id}`,
                method: "DELETE",
                success: function () {
                    loadBooks();
                    showMessage("Book deleted successfully.", "success");
                },
                error: function (xhr) {
                    showMessage(`Failed to delete book: ${xhr.responseText}`, "error");
                },
            });
        }
    });

    $("#book-form-element").submit(function (event) {
        event.preventDefault();

        const id = $("#book-id").val();
        const book = {
            title: $("#title").val(),
            author: $("#author").val(),
            published_date: $("#published_date").val(),
            isbn: $("#isbn").val(),
            pages: $("#pages").val(),
        };

        if (!book.title || !book.author || !book.published_date || !book.isbn || !book.pages) {
            showMessage("Please fill in all fields.", "error");
            return;
        }

        if (!/^\d{4}-\d{2}-\d{2}$/.test(book.published_date)) {
            showMessage("Published Date must be in the format YYYY-MM-DD.", "error");
            return;
        }

        function handleErrorResponse(xhr) {
            let errorMsg = "Failed to process request";
            if (xhr.responseJSON && xhr.responseJSON.detail) {
                if (Array.isArray(xhr.responseJSON.detail)) {
                    errorMsg = xhr.responseJSON.detail.map((err) => err.msg).join("; ");
                } else {
                    errorMsg = xhr.responseJSON.detail;
                }
            }
            showMessage(errorMsg, "error");
        }

        if (id) {
            $.ajax({
                url: `/books/${id}`,
                method: "PUT",
                contentType: "application/json",
                data: JSON.stringify(book),
                success: function () {
                    loadBooks();
                    $("#book-form").hide();
                    showMessage("Book updated successfully.", "success");
                },
                error: function (xhr) {
                    handleErrorResponse(xhr);
                },
            });
        } else {
            $.ajax({
                url: "/books",
                method: "POST",
                contentType: "application/json",
                data: JSON.stringify(book),
                success: function () {
                    loadBooks();
                    $("#book-form").hide();
                    showMessage("Book added successfully.", "success");
                },
                error: function (xhr) {
                    handleErrorResponse(xhr);
                },
            });
        }
    });

    loadBooks();
});
