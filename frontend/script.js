/* =========================================================
   LEGISWATCH
   FRONTEND JAVASCRIPT
========================================================= */


/* =========================================================
   ELEMENTS
========================================================= */

const checkButton =
    document.getElementById("checkButton");

const buttonText =
    document.getElementById("buttonText");

const statusText =
    document.getElementById("status");

const emailInput =
    document.getElementById("emailInput");

const results =
    document.getElementById("results");

const emptyState =
    document.getElementById("emptyState");

const resultCount =
    document.getElementById("resultCount");

const searchInput =
    document.getElementById("searchInput");

const searchButton =
    document.getElementById("searchButton");

const previousButton =
    document.getElementById("previousButton");

const nextButton =
    document.getElementById("nextButton");

const pageNumber =
    document.getElementById("pageNumber");


/* =========================================================
   LANGUAGE BUTTONS
========================================================= */

const languageGeorgian =
    document.getElementById("languageGeorgian");

const languageEnglish =
    document.getElementById("languageEnglish");


/* =========================================================
   SETTINGS
========================================================= */

const API_URL =
    "https://legiswatch-production.up.railway.app";

const limit = 5;

let currentPage = 1;

let currentSearch = "";

let currentLanguage =
    localStorage.getItem("legiswatchLanguage") || "en";


/* =========================================================
   TRANSLATIONS
========================================================= */

const translations = {

    ka: {

        header: {

            tagline:
                "STAY INFORMED. TRACK WHAT MATTERS."

        },


        nav: {

            home:
                "მთავარი",

            legislation:
                "კანონმდებლობა",

            about:
                "ჩვენ შესახებ",

            howItWorks:
                "როგორ მუშაობს"

        },


        hero: {

            title: `
                საკანონმდებლო<br>
                ინიციატივები<br>
                <span style="color: #bf0603;">LIVE</span> რეჟიმში
            `,

            description:
                "LegisWatch გაძლევთ შესაძლებლობას რეალურ დროში აკონტროლოთ ახალი საკანონმდებლო ინიციატივები.",

            emailPlaceholder:
                "შეიყვანე ელფოსტა",

            checkUpdates:
                "განახლებების შემოწმება"

        },


        features: {

            track: {

                title:
                    "თვალი ადევნე ახალ ინიციატივებს",

                description:
                    "თვალი ადევნე საქართველოს პარლამენტში რეგისტრირებულ ახალ საკანონმდებლო ინიციატივებს."

            },


            realtime: {

                title:
                    "განახლებები რეალურ დროში",

                description:
                    "მიიღე პარლამენტთან დაკავშირებული უახლესი ინფორმაცია ერთ სივრცეში."

            },


            open: {

                title:
                    "ღია და გამჭვირვალე",

                description:
                    "მიიღე ოფიციალურ საკანონმდებლო ინფორმაციაზე წვდომა მარტივი და გასაგები ინტერფეისით."

            }

        },


        about: {

            label:
                "LEGISWATCH-ის შესახებ",

            title:
                "კანონმდებლობა მარტივად და გასაგებად.",

            lead:
                "LegisWatch საშუალებას გაძლევს, მარტივად ადევნო თვალი საქართველოს საკანონმდებლო ინიციატივებს.",

            description:
                "პლატფორმა აკვირდება საქართველოს პარლამენტში ახლად რეგისტრირებულ საკანონმდებლო ინიციატივებს და ოფიციალურ ინფორმაციას ერთ, მარტივად და გასაგებად წარმოდგენილ სივრცეში აერთიანებს.",

            follow:
                "სხვადასხვა გვერდისა და დოკუმენტის ცალ-ცალკე ძიების ნაცვლად, მომხმარებლებს შეუძლიათ სწრაფად მიიღონ ინფორმაცია უახლესი ინიციატივების შესახებ და თვალი ადევნონ მათ ცვლილებებს."

        },


        process: {

            label:
                "როგორ მუშაობს",

            title:
                "პარლამენტიდან შენს ეკრანზე",


            monitor: {

                title:
                    "მონიტორინგი",

                description:
                    "LegisWatch ამოწმებს პარლამენტის ოფიციალურ ინფორმაციას და აკვირდება ახლად რეგისტრირებულ საკანონმდებლო ინიციატივებს."

            },


            organize: {

                title:
                    "ორგანიზება",

                description:
                    "საკანონმდებლო ინფორმაცია გროვდება და მარტივ, გასაგებ ფორმატში ორგანიზდება."

            },


            follow: {

                title:
                    "თვალყურის დევნება",

                description:
                    "მომხმარებლებს შეუძლიათ სწრაფად და მარტივად იპოვონ საინტერესო ინიციატივები და მიიღონ ინფორმაცია მათ შესახებ ავტომატურ რეჟიმში."

            }

        },


        legislation: {

            title:
                "უახლესი საკანონმდებლო ინიციატივები",

            description:
                "საქართველოს პარლამენტის უახლესი კანონპროექტები და განახლებები.",

            viewAll:
                "ყველა საკანონმდებლო ინიციატივა →",

            searchPlaceholder:
                "მოძებნე საკანონმდებლო ინიციატივა...",

            searchButton:
                "ძიება",

            resultCount:
                "0 შედეგი",

            emptyTitle:
                "საკანონმდებლო ინიციატივა ვერ მოიძებნა",

            emptyDescription:
                "სცადე სხვა საძიებო სიტყვა.",

            previous:
                "← წინა",

            next:
                "შემდეგი →"

        },


        testNotice: {

            label:
                "ტესტირების რეჟიმი",

            description:
                "LegisWatch ამჟამად მუშაობს განვითარების და ტესტირების გარემოში."

        },


        footer: {

            tagline:
                "საქართველოს საკანონმდებლო მონიტორინგი",

            home:
                "მთავარი",

            legislation:
                "კანონმდებლობა",

            about:
                "ჩვენ შესახებ"

        },


        messages: {

            loading:
                "იტვირთება...",

            unableToLoad:
                "საკანონმდებლო ინიციატივების ჩატვირთვა ვერ მოხერხდა",

            tryAgainLater:
                "გთხოვთ, სცადოთ მოგვიანებით.",

            noResults:
                "საკანონმდებლო ინიციატივა ვერ მოიძებნა",

            tryAnotherSearch:
                "სცადე სხვა საძიებო სიტყვა.",

            showing:
                "ნაჩვენებია",

            pleaseEnterEmail:
                "გთხოვთ, შეიყვანოთ ელფოსტის მისამართი.",

            invalidEmail:
                "გთხოვთ, შეიყვანოთ ელფოსტის სწორი მისამართი.",

            checking:
                "მოწმდება...",

            checkingData:
                "პარლამენტის მონაცემები მოწმდება...",

            updateSuccess:
                "განახლებები წარმატებით შემოწმდა. გთხოვთ, შეამოწმოთ ელფოსტა.",

            updateError:
                "განახლებების შემოწმება ვერ მოხერხდა. გთხოვთ, სცადოთ თავიდან.",

            somethingWentWrong:
                "რაღაც შეცდომა მოხდა.",

            checkUpdates:
                "განახლებების შემოწმება"

        }

    },


    en: {

        header: {

            tagline:
                "STAY INFORMED. TRACK WHAT MATTERS."

        },


        nav: {

            home:
                "HOME",

            legislation:
                "LEGISLATION",

            about:
                "ABOUT",

            howItWorks:
                "HOW IT WORKS"

        },


        hero: {

            title: `
                GEORGIAN<br>
                LEGISLATION<br>
                TRACKED <span style="color: #bf0603;">LIVE</span>
            `,

            description:
                "LegisWatch helps you track new laws, draft bills and parliamentary updates from the Parliament of Georgia — clearly, simply, and in real time.",

            emailPlaceholder:
                "Enter your email",

            checkUpdates:
                "CHECK FOR UPDATES"

        },


        features: {

            track: {

                title:
                    "TRACK NEW LEGISLATION",

                description:
                    "Follow newly registered legislative initiatives from the Parliament of Georgia."

            },


            realtime: {

                title:
                    "REAL-TIME UPDATES",

                description:
                    "Keep track of the latest parliamentary information in one place."

            },


            open: {

                title:
                    "OPEN & TRANSPARENT",

                description:
                    "Access official legislative information through a clear and simple interface."

            }

        },


        about: {

            label:
                "ABOUT LEGISWATCH",

            title:
                "LEGISLATION<br>MADE CLEAR.",

            lead:
                "LegisWatch makes Georgian legislation easier to follow.",

            description:
                "The platform monitors newly registered legislative initiatives and presents official parliamentary information in one clear and accessible place.",

            follow:
                "Instead of searching through different pages and documents, users can quickly discover recent initiatives and follow their development."

        },


        process: {

            label:
                "HOW IT WORKS",

            title:
                "FROM PARLIAMENT<br>TO YOUR SCREEN.",


            monitor: {

                title:
                    "MONITOR",

                description:
                    "LegisWatch checks official parliamentary information for newly registered legislative initiatives."

            },


            organize: {

                title:
                    "ORGANIZE",

                description:
                    "Legislative information is collected and organized into a simple and readable format."

            },


            follow: {

                title:
                    "FOLLOW",

                description:
                    "Users can quickly discover legislation and open the official parliamentary source."

            }

        },


        legislation: {

            title:
                "RECENT LEGISLATION",

            description:
                "Latest bills and updates from the Parliament of Georgia.",

            viewAll:
                "VIEW ALL LEGISLATION →",

            searchPlaceholder:
                "Search legislation...",

            searchButton:
                "SEARCH",

            resultCount:
                "0 results",

            emptyTitle:
                "No legislation found",

            emptyDescription:
                "Try another search.",

            previous:
                "← PREVIOUS",

            next:
                "NEXT →"

        },


        testNotice: {

            label:
                "TEST MODE",

            description:
                "LegisWatch is currently operating in a development and testing environment."

        },


        footer: {

            tagline:
                "Georgian Legislative Monitoring",

            home:
                "HOME",

            legislation:
                "LEGISLATION",

            about:
                "ABOUT"

        },


        messages: {

            loading:
                "Loading...",

            unableToLoad:
                "Unable to load legislation",

            tryAgainLater:
                "Please try again later.",

            noResults:
                "No legislation found",

            tryAnotherSearch:
                "Try another search.",

            showing:
                "Showing",

            pleaseEnterEmail:
                "Please enter your email address.",

            invalidEmail:
                "Please enter a valid email address.",

            checking:
                "CHECKING...",

            checkingData:
                "Checking parliamentary data...",

            updateSuccess:
                "Updates checked successfully. Please check your email.",

            updateError:
                "Unable to check updates. Please try again.",

            somethingWentWrong:
                "Something went wrong.",

            checkUpdates:
                "CHECK FOR UPDATES"

        }

    }

};


/* =========================================================
   TRANSLATION HELPER
========================================================= */

function t(key) {

    const parts =
        key.split(".");

    let value =
        translations[currentLanguage];

    for (const part of parts) {

        value =
            value?.[part];

    }

    return value ?? key;
}


/* =========================================================
   APPLY TRANSLATIONS
========================================================= */

function applyTranslations() {

    document.documentElement.lang =
        currentLanguage;


    document
        .querySelectorAll("[data-i18n]")
        .forEach(function (element) {

            const key =
                element.getAttribute(
                    "data-i18n"
                );

            element.innerHTML =
                t(key);

        });


    document
        .querySelectorAll("[data-i18n-placeholder]")
        .forEach(function (element) {

            const key =
                element.getAttribute(
                    "data-i18n-placeholder"
                );

            element.placeholder =
                t(key);

        });


    languageGeorgian.classList.toggle(
        "active",
        currentLanguage === "ka"
    );


    languageEnglish.classList.toggle(
        "active",
        currentLanguage === "en"
    );

}


/* =========================================================
   CHANGE LANGUAGE
========================================================= */

function setLanguage(language) {

    if (
        language !== "ka" &&
        language !== "en"
    ) {

        return;

    }


    currentLanguage =
        language;


    localStorage.setItem(
        "legiswatchLanguage",
        currentLanguage
    );


    applyTranslations();

}


/* =========================================================
   LANGUAGE BUTTONS
========================================================= */

languageGeorgian.addEventListener(
    "click",
    function () {

        setLanguage("ka");

    }
);


languageEnglish.addEventListener(
    "click",
    function () {

        setLanguage("en");

    }
);


/* =========================================================
   LOAD LEGISLATION
========================================================= */

async function loadBills() {

    const offset =
        (currentPage - 1) * limit;


    const url =
        `${API_URL}/bills` +
        `?limit=${limit}` +
        `&offset=${offset}` +
        `&search=${encodeURIComponent(currentSearch)}`;


    results.style.display =
        "none";


    emptyState.style.display =
        "none";


    resultCount.textContent =
        t("messages.loading");


    try {

        const response =
            await fetch(url);


        if (!response.ok) {

            throw new Error(
                "Failed to load legislation."
            );

        }


        const bills =
            await response.json();


        renderBills(bills);

    }
    catch (error) {

        console.error(error);


        results.innerHTML =
            "";


        results.style.display =
            "none";


        emptyState.style.display =
            "block";


        emptyState.innerHTML = `
            <h3>
                ${t("messages.unableToLoad")}
            </h3>

            <p>
                ${t("messages.tryAgainLater")}
            </p>
        `;


        resultCount.textContent =
            currentLanguage === "ka"
                ? "0 შედეგი"
                : "0 results";

    }

}


/* =========================================================
   RENDER LEGISLATION
========================================================= */

function renderBills(bills) {

    results.innerHTML =
        "";


    if (bills.length === 0) {

        results.style.display =
            "none";


        emptyState.style.display =
            "block";


        emptyState.innerHTML = `
            <h3>
                ${t("messages.noResults")}
            </h3>

            <p>
                ${t("messages.tryAnotherSearch")}
            </p>
        `;


        resultCount.textContent =
            currentLanguage === "ka"
                ? "0 შედეგი"
                : "0 results";


        previousButton.disabled =
            currentPage === 1;


        nextButton.disabled =
            true;


        pageNumber.textContent =
            currentPage;


        return;

    }


    emptyState.style.display =
        "none";


    results.style.display =
        "block";


    const start =
        (currentPage - 1) * limit + 1;


    const end =
        start + bills.length - 1;


    resultCount.textContent =
        `${t("messages.showing")} ${start}–${end}`;


    bills.forEach(
        function (bill) {

            const billUrl =
                `bill?id=${bill.bill_id}`;


            const row =
                document.createElement(
                    "article"
                );


            row.className =
                "bill-row";


            row.innerHTML = `

                <div class="bill-name">

                    ${escapeHTML(
                        bill.bill_name
                    )}

                </div>


                <div>

                    <span class="bill-status">

                        ${escapeHTML(
                            bill.bill_type
                        )}

                    </span>

                </div>


                <div class="bill-info">

                    ${escapeHTML(
                        bill.registration_number
                    )}

                </div>


                <div class="bill-info">

                    ${escapeHTML(
                        bill.registration_date
                    )}

                </div>


                <div class="bill-arrow">

                    <a
                        href="${billUrl}"
                        aria-label="View bill details"
                    >

                        →

                    </a>

                </div>

            `;


            /* =================================================
               WHOLE ROW CLICKABLE
            ================================================= */

            row.addEventListener(
                "click",
                function (event) {

                    if (
                        event.target.closest(
                            "a"
                        )
                    ) {

                        return;

                    }


                    window.location.href =
                        billUrl;

                }
            );


            results.appendChild(
                row
            );

        }
    );


    pageNumber.textContent =
        currentPage;


    previousButton.disabled =
        currentPage === 1;


    nextButton.disabled =
        bills.length < limit;

}


/* =========================================================
   SEARCH
========================================================= */

searchButton.addEventListener(
    "click",
    function () {

        currentSearch =
            searchInput.value.trim();


        currentPage =
            1;


        loadBills();

    }
);


/* =========================================================
   ENTER = SEARCH
========================================================= */

searchInput.addEventListener(
    "keydown",
    function (event) {

        if (event.key === "Enter") {

            currentSearch =
                searchInput.value.trim();


            currentPage =
                1;


            loadBills();

        }

    }
);


/* =========================================================
   PAGINATION
========================================================= */

nextButton.addEventListener(
    "click",
    function () {

        currentPage++;


        loadBills();

    }
);


previousButton.addEventListener(
    "click",
    function () {

        if (currentPage > 1) {

            currentPage--;


            loadBills();

        }

    }
);


/* =========================================================
   CHECK FOR UPDATES
========================================================= */

checkButton.addEventListener(
    "click",
    async function () {

        const email =
            emailInput.value.trim();


        if (email === "") {

            statusText.textContent =
                t("messages.pleaseEnterEmail");


            emailInput.focus();


            return;

        }


        if (
            !email.includes("@") ||
            !email.includes(".")
        ) {

            statusText.textContent =
                t("messages.invalidEmail");


            emailInput.focus();


            return;

        }


        checkButton.disabled =
            true;


        buttonText.textContent =
            t("messages.checking");


        statusText.textContent =
            t("messages.checkingData");


        try {

            const response =
                await fetch(
                    `${API_URL}/check-updates`,
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify({
                            email: email
                        })
                    }
                );


            const data =
                await response.json();


            if (!response.ok) {

                throw new Error(
                    data.detail ||
                    t(
                        "messages.somethingWentWrong"
                    )
                );

            }


            statusText.textContent =
                t("messages.updateSuccess");

        }
        catch (error) {

            console.error(error);


            statusText.textContent =
                t("messages.updateError");

        }
        finally {

            buttonText.textContent =
                t("messages.checkUpdates");


            checkButton.disabled =
                false;

        }

    }
);


/* =========================================================
   HTML SAFETY
========================================================= */

function escapeHTML(value) {

    return String(
        value ?? ""
    )

        .replaceAll(
            "&",
            "&amp;"
        )

        .replaceAll(
            "<",
            "&lt;"
        )

        .replaceAll(
            ">",
            "&gt;"
        )

        .replaceAll(
            '"',
            "&quot;"
        )

        .replaceAll(
            "'",
            "&#039;"
        );

}


/* =========================================================
   INITIAL LANGUAGE
========================================================= */

setLanguage(currentLanguage);


/* =========================================================
   INITIAL LOAD
========================================================= */

loadBills();