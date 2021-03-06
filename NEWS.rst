0.8.4 (2016-02-17):
  - Remove unused `nevow.livepage` support code; fixes compatibility with Nevow
    0.13.0.
  - `StringEndpointPort` ports are now deletable from the commandline (with
    the `axiomatic port delete` command).
  - Mantissa's CI now tests against Twisted trunk, for early warnings of
    breakage.

0.8.3 (2015-10-23):
  - StringEndpointPort was still broken, somehow. It really works now, promise!

0.8.2 (2015-09-04):
  - Fix a major issue with the last few releases which resulted in a number of
    static files not being installed and/or missing from the source tarball.
  - Somewhat related to the previous issue, the tests no longer fail when
    running from an installed copy due to the documentation / examples being
    missing (these are not installed into site-packages).

0.8.1 (2015-07-20):
  - Fix some issues with the new StringEndpointPort which, among other things,
    rendered it completely broken.
  - Fix a test failure on versions of Twisted with the new logging system.

0.8.0 (2015-06-01):
  - Fix the JavaScript function for linkifying a block of text so that it
    doesn't drop all the text following the last link in the text.
  - Fix compatibility with modern versions of Twisted.
  - Fix compatibility with modern versions of cssutils.
  - Add a new port type, StringEndpointPort, which is now used by
    `axiomatic port`. This now allows using any endpoint type supported by the
    string endpoint parser in Twisted (which is extensible through plugins).
  - PyPy is now supported and should be fully functional (although there has
    not been much real-world testing of this yet).
  - Switch to setuptools; pip installation should be much easier now.

0.7.0 (2009-11-25):
  - Add an SSH application server.
  - Add a SQLite3 FTS3-based fulltext search backend.
  - Change a bad failure mode of `xmantissa.websharing.linkTo` to a better
    one with more useful information.
  - Add documentation covering interstore messaging.
  - Fix the JavaScript module caching added in the last release.

0.6.22 (2008-12-09):
  - Admin powerup added for exposing statistics information over AMP.
  - Changed the Mantissa AMP server so that it doesn't associate
    application protocols with a box sender until it has sent the
    response to the route setup command.
  - Added support for AMP authentication via one-time pads, and a
    facility for generation of one-time pads.

0.6.21 (2008-10-02):
  - Contact types can now have their edit forms rendered as siblings
    of the giant Mantissa edit form.
  - The root resource can now be configured to display the toplevel
    public page shared by a given offering.
  - Fixed argument ordering bug in "add person" javascript.
  - Fixed the definition of IOffering to match the actual offering
    interface.
  - Comprehensive reworking of how URLs are managed by Mantissa, with
    the introduction of the new IWebViewer interface. Shared items may
    now provide non-live adapters and IResource adapters.
  - Pluggable AMP server added based on the AMP routing facilities in
    Epsilon.

0.6.20 (2008-08-12):
  - Mugshot thumbnail generation:  avoid aliasing paletted and bicolor images.
  - Better support for IRIs.
  - Website code refactored, moving some of its functionality into
    xmantissa.web.SiteConfiguration.
  - Fixed several bugs in the region-model scrolltable related to text
    sort-columns.
  - Support added for name-based virtual hosting for per-user
    subdomains.
  - Person mugshots now shown in address book scrolltable.
  - Person creation and contact info creation are now separate steps.
  - 'axiomatic port' command added for general listening-port
    configuration.
  - IPublicPage is now deprecated, in favor of using the sharing
    system for providing public pages from app stores.

0.6.19 (2008-02-19):
  - The Mantissa People mugshot placeholder image has been updated and
    the placeholder code refactored.

0.6.18 (2008-02-06):
  - Added a renderer which exposes the value of WebSite.rootURL and
    added a base tag to the shell template which sets that URL as
    the base for links on the page.
  - Implemented a session-wrapper hook in Mantissa's
    PersistentSessionWrapper to base the domain parameter of the
    session cookie on the domains the site is configured with and a
    flag indicating whether the cookie should be valid for subdomains.

0.6.18 (2008-01-18):
  - Introduced an API for filtering lists of people, and some UI for
    doing this with your address book.
  - ShareIDs can now contain non-ASCII characters.
  - The implementation of WebSite.rootURL has changed so that it
    considers the Host header of the request when constructing the URL
    to return.  Requests made to unrecognized hosts will now have a
    root URL which is absolute and includes the configured hostname of
    the WebSite.  This allows name-based virtual hosting to work
    without requiring all static content to be served beneath the
    virtual host domain name.  Requests made to recognized hosts will
    continue to use relative URLs with absolute paths.
  - Mantissa's Offering interface now includes support for the
    definition of the root of an offering's static content and this is
    now served without requiring a session.
  - Offerings are now managed using an object implementing a new
    mantissa interface rather than with free functions.
  - The base XHTML directory theme class now supports a simpler API
    for adding a stylesheet to the head of pages.
  - Many classes now use ThemedDocumentFactory rather than trying to
    load a document factory directly.
  - PrivateApplication.getDocFactory now only returns loaders from
    themes for installed offerings instead of considering all
    offerings available to the system.

0.6.17 (2008-01-16):
  - IContactType implementations are now allowed to arrange their
    contact items into named groups.  The structure of these groups
    affects the rendering of read-only views.

0.6.16 (2008-01-02):
  - A basic person import widget has been added.
  - Support for inserting Google Analytics tracking code into Mantissa
    pages has been added.

0.6.15 (2006-12-06):
  - IContactTypes can now declare that particular contact items cannot
    be edited by the user.

0.6.14 (2007-12-04):
  - Use of _getLoader has been replaced with SiteTemplateResolver.
  - EmailAddress items are now created for newly created users when
    UserInfoSignup is being used.
  - Security problem fixed in xmantissa.webtheme that could allow
    access to arbitrary filesystem contents.

0.6.13 (2007-11-27):
  - An IContactType implementation has been added for the PhoneNumber
    and Notes items.
  - The 'start menu' has been removed from the global nav, along with
    many unnecessary tabs.
  - The addressbook's initial state can now be specified in its URL.
  - Sharing now supports Unicode URIs.
  - The "me" person is now rendered uniquely in the addressbook.
  - The addressbook widget is now bigger.

0.6.12 (2007-11-13):
  - The mugshot upload form is now rendered in an iframe,
    and renders the current mugshot alongside it.

0.6.11 (2007-11-09):
  - Usernames now do not have their domain rendered when viewed on a page
    served from that domain.

0.6.10 (2007-11-07):
  - Made the Required User Information Signup page a bit clearer about
    what the user has to do next. Instead of depositing the user
    directly on the login page, make sure that they know that they've
    succeded, and then ask them to sign in by clicking on a link.
  - Made the Mantissa "Address Book" look a whole lot nicer.  The most
    visible change is the introduction of a two-pane view, with a list
    of people in a scrolltable, and an area where read-only Person
    views and Person edit forms are rendered.
  - Added a 'settings' link to the global nav.

0.6.9 (2007-11-02):
  - Made the mugshot thumbnail image larger.
  - Allowed IContactTypes to declare they don't support multiple
    contact items per person.
  - Ensured that the login page comes from a template in an offering
    that is actually installed.
  - Fixed webnav.getTabs to respect Tab.linkURL on primary nav
    elements.
  - Eliminated the separate public-shell and navigation templates.
    Instead, the shell template is now used to define both public and
    private views and to define the navigation.
  - Deprecated scrolltable.UnsortableColumn in favor of
    scrolltable.UnsortableColumnWrapper.
  - Public-page-wrapped fragments can now specify the page title.
  - Bogus email addresses used for password reset are handled better
    now.
  - Password reset form styling updated.

0.6.8 (2007-10-16):
  - website.WebSite.maybeEncryptedRoot deprecated in favor of
    website.WebSite.rootURL. CSS is now served using the same URL
    scheme as the page including it.
  - "Private" mantissa navigation/menubar now displayed on share pages
    when the viewer is authenticated.
  - LiveForm coercers may now return Deferreds and processing of the
    form will be delayed until these Deferreds are called back.
  - Added a new IOrganizerPlugin callback: "contactItemEdited".
  - Improvements to repeated forms.

0.6.7 (2007-09-05):
  - A bug preventing mugshot uploads was fixed.
  - The scrolltable now only requests more rows when the user can see blank
    space.
  - Multiple pieces of contact info can be added at person creation time now.
  - Share items are now deleted when the item they are sharing is deleted.
  - A bug preventing the contact info edit from from being submitted multiple
    times was fixed.
  - Client-side removal of repeated liveform elements is now possible.
  - A bug occasionally causing regions in the scrolltable to overlap was fixed.
  - Store owner Person objects are now created with their name attributes set
    based on the name provided in UserInfoSignup, if available.
  - Functionality for shared items can now be externally defined, via adapters.
  - Person.name is now case insensitive.
  - A method has been added to IOrganizerPlugin for observing changes to the
    name attribute of Person items.
  - Themes and JavaScript modules are no longer reloaded from disk if they are
    changed while the server is running.
  - Athena modules served by MantissaLivePage now are served over the same
    protocol as the page which requires them.
  - The 'RealName' contact type has been removed.
  - UserInfoSignup now prompts for name in a single field rather than in
    first/last name fields.
  - The address book's person scrolltable is now ordered by Person.name.
  - Error message when installing offerings fixed. Hooray!
  - Various JavaScript optimizations.

0.6.6 (2007-08-01):
  - UserInfoSignup now stores firstname/lastname in the user store.
  - The stats powerup no longer starts itself automatically, to prevent it from
    interfering with unit tests.
  - Duplicate Person nicknames are now prevented.
  - people.Person now has a 'vip' attribute, displayed in the person
    scrolltable in the address book.
  - The address book add-person form now shows details about a person
    immediately after it is created.
  - liveform.LiveForm now has a 'compact' method, which causes it to switch to
    the compact liveform template (including all its subforms).
  - Added an InputError exception to LiveForm which can be used by
    server-side components to indicate an input verification failure to the
    client.  Also added logic to the client to handle this kind of error
    specially.
  - sharing.asAccessibleTo now yields the correct results when dealing with a
    query with a limit.
  - Added a LiveForm parameter type list parameter type, which allows a subform
    to be repeated an arbitrary number of times inside its parent.
  - Further improvements made to the new scrolltable, including a timestamp
    column, a client-side widget column, better pluggability, bugfixes, and
    better test coverage.
  - The scrolltable will now tell you when it is loading rows, including an
    initial loading notification so that the page will immediately have some
    feedback visible rather than just a blank area where the scrolltable is
    supposed to be.

0.6.5 (2007-07-06):
  - People are now editable.
  - Add/delete buttons added to the person scrolltable.
  - People now include 'postal contact' fields.
  - Multiple email-address contact items' creation is now prevented.
  - An event publisher for the creation of new contacts has been
    added.
  - Theme lookup now cached during page rendering, both for calls to
    the deprecated webtheme.getLoader and via ThemedElement.
  - New inequality-based scrolltable implementation.
  - Themeing support for Athena's "unsupported browser" page now
    provided.
  - JavaScript modules now served from a centralized location for
    public and private pages.

0.6.4 (2007-06-06):
  - LoginPage now remembers and passes on query arguments.
  - Removed use of deprecated API from webadmin.DeveloperSite.

0.6.3 (2007-05-24):

  - Added a method to IOrganizerPlugin to allow notification of
    creation of new person objects.
  - Added a method to IOrganizerPlugin to allow extension of the
    add-person form with new contact information types.
  - Liveform refactoring.

0.6.2 (2007-04-27):
  - Data passed to Lucene for indexing or search queries is now
    filtered to prevent email addresses and URLs from being recognized
    as single tokens.
  - The sharing API has been significantly revised.
  - PyLucene result sets can now be manipulated without loading large
    numbers of hit objects.

0.6.1 (2007-02-23):
  - Selection and activation tracking has been moved out of Quotient
    and into Mantissa.ScrollTable.
  - Autocomplete has been added, from Quotient.
  - Significant improvements to sharing.
  - webapp.PrivateApplication.__init__ has been removed, in order to
    prevent its privateKey from changing upon upgrade.

0.6.0 (2007-01-23):
  - Several upgraders left out of the previous release have been added.

0.5.27 (2007-01-11):
  - Benefactors have been  removed. Powerups are directly selected by admins
    and grouped into Products (as defined in xmantissa.product). Products 
    are associated with signup mechanisms now, rather than benefactor factories.

    When Products are installed on user stores, Installation items are created 
    to track the installed powerups. Installations may be suspended, which will
    disable the rendering of the web interface of their powerups. Unsuspension 
    will restore them to visibility.

  - Add xmantissa.port module which provides two item classes, TCPPort and
    SSLPort, which can be used to set up and tear down network services in
    a general manner, removing the need to implement service and port logic
    at each point where a TCP or SSL server is desired.

    Provide a web interface for administrators to create and destroy these
    ports in a general way, making network service configuration for all
    mantissa applications that much richer.

    Update command line tools to deal with this change as well, but they do
    not expose the complete flexibility of the new system.
  
    Take note, certificates for SSL services have been copied to a new 
    location in this upgrade. This leaves the original certificate file 
    unchanged but mostly unused.

  - The "Add Person" form will now ensure that only one person can exist with
    any given email address.
    
0.5.26 (2006-12-08):
  - Stylesheets work on HTTP-only servers again.
  - User info signup gives more feedback on why invalid input is rejected.
  - Prefs forms are redisplayed after submission rather than "[Object object]"
  - Only domains currently hosted by the server will be accepted as host parts
    for new usernames.
  - Improved range checking in ScrollTable to avoid IndexErrors.  Also reset
    the scroll tracking property when a ScrollTable is emptied.

0.5.25 (2006-11-22):
  - Images, Javascript and CSS are now served over HTTPS when the page is.

0.5.24 (2006-11-20):
  - Added a method for retrieving all of the email addresses associated with a
    Person.
  - Removed unnecessary attributes from ItemQueryScrollingFragment and
    documented the required IColumn attribute, attributeID.

0.5.23 (2006-11-17):
  - Trivial changes to the scrolltable API.

0.5.22 (2006-11-08):
  - Mantissa CSS now uses the same style for :link and :visit.
  - Improved signup and password reset behaviour.
  - Title of the settings page changed to "Settings".
  - Fixed an issue where scrolling around or calling emptyAndRefill() in
    certain situations would generate a phantom scroll event which would
    result in the scrolltable ignoring subsequent scrolls.

0.5.21 (2006-10-31):
  - A sort direction parameter has been added to the search API.
  - Further scrolltable refactoring, improving the UI, creating placeholder
    rows faster, and awareness of row removal in the placeholder model.

0.5.20 (2006-10-21):
  - Scrolltable now supports conditionally enabled actions.
  - Search now handles charsets properly.
  - People are now sorted by last name.

0.5.19 (2006-10-17):
  - Mantissa no longer depends on Xapian.
  - Password reset link fixed.
  - An API for setting liveform values from javascript has been added.
  - Scrolltable has been reverted to the previous version for performance
    reasons.

0.5.18 (2006-10-10):
  - Better looking scrolltables.
  - Liveform success notification is now faster.

0.5.17 (2006-10-05):
  - Login and signup are now done over HTTPS when available.

0.5.16 (2006-09-26):
  - Signup form now generates valid email localparts for usernames, and
    doesn't allow invalid usernames to be submitted.
  - Client-side actions API added for scroltables.
  - Searching fixes; indexed items can now control how they're sorted.

0.5.15 (2006-09-20):
  - Fulltext indexer doesn't use stopwords now, and adds all other fields
    to the 'text' part of the document also.
  - added PostalAddress and Nots fields to Person.
  - Login form now links to password reset.

0.5.14 (2006-09-12):
  - ScrollTable has been refactored; more methods return Deferreds, and an API
    for removing rows has been added.
  - UI improvements and bugfixes.

0.5.13 (2006-08-30):
  - Signup editor now allows deletion of signup pages.
  - Various UI and bug fixes.

0.5.12 (2006-08-22):
  - Better IE support.
  - A bug in the user-info signup page that could render the form 
    unsubmittable was fixed.
  - Simpler preferences API.
  - Shinier tabs.

0.5.11 (2006-08-14):
  - the URL / now redirects to /private for authenticated users.
  - The view and model portions of ScrollableFragment have been factored
    into separate classes.
  - The fulltext indexer no longer stores the text parts of the documentss it
    indexes. Additionally, it tags each document with its type.
  - MochiKit is now included, since Nevow doesn't bundle it anymore.

0.5.10 (2006-07-18):
  - A facility for making URLs that will display the web facet of an item
    while showing some other tab as being selected has been added, and is
    used for Person links.

0.5.9 (2006-07-17):
  - A document preprocessor is now used to make static web content more 
    cacheable.

0.5.8 (2006-07-14):
  - Updates to mugshot code.
  - Bugfixes in LiveForm javascript.

0.5.7 (2006-07-08):
  - Updated all templates to use Element instead of Fragment.

0.5.6 (2006-07-05):
  - People image thumbnails are smaller.
  - Users are now sent to their private page after login.
  - Use Nevow's new Element class instead of Fragment.
  - Various unit test improvements and bugfixes.

0.5.5 (2006-06-27):
  - A new signup UI has been added.

0.5.4 (2006-06-26):
  - An index has been added to the stats database to reduce startup time.

0.5.3 (2006-06-23):
  - UI fixes: #1009, #1173, #1187

0.5.2 (2006-06-20):
  - Query-stats graph changed to not hit the database on every update.
  - Searches can now be restricted to certain fields in indexed documents.
  - Various UI fixes.

0.5.1 (2006-06-16):
  - Updated navigation, plus improved functionality in IE.

0.5.0 (2006-06-12):
  - A number of bugfixes and minor functionality changes.
  - added LiveForm, a layer to automate processing simple forms with Athena
    LivePage.
  - added a "sharing" system, for controlling permissions on publicly published
    database objects, and a "websharing" system, for creating a public page and
    publishing items on it by ID, displaying different items for a particular
    ID based on who is viewing it
  - Moved most URLs from ad-hoc /static hierarchy to new application-based
    hierarchy, e.g. /Mantissa, /Quotient, etc.
  - vastly different navigation
  - full-text index and search support, with hype, xapian, and pylucene
    backends.
  - administrative interactive statistics view
  - tools for adding and removing account features interactively
  - new signup mechanism that allows the user to see whether their inputs are
    valid in real-time
  - migrate (almost) every list view of data to use scrolltable rather than
    the page-based tabular data browser.
  - password-reset page (although this is not linked from anywhere)
  - appropriate version numbers are now displayed on every page
  - fixed various issues with "tab" ordering in the navigation system
  - 'axiomatic web' command-line tool no longer makes spurious database
    changes.

0.4.1 (2005-12-20):
  - Include accidentally omitted nevow plugins in release tarball.

0.4.0 (2005-12-20):
  - Added --http-log parameter to Axiomatic "web" subcommand
  - Added InstallableMixin which implements necessary logic to simplify
    making installOn idempotent.
  - Various uses of deprecated APIs fixed, along with other code-cleanliness
    fixes.
  - Invalid public URLs now 404 instead of 500.
  - Added a generalized "Tabular Data Browser" (TDB) Fragment which can be
    used to display any Axiom query on a web page.
  - Added a very simple, extensible abstraction for tracking various data
    that is person-oriented.
  - An "Offering" system has been added, greatly simplifying the process of
    writing a new application which plugs into a Mantissa server.
  - A new axiomatic plugin has been added, "project", which emits a skeleton
    Offering plugin, suitable for use as a starting point for developing a
    Mantissa application.
  - The administrative account can now browse user accounts.

0.3.1 (2005-11-05):
  - Fix packaging bug - include axiom plugins

0.3.0 (2005-11-02):
  - Improved output of 'axiomatic web --list'
  - Render 'log in' link when user is not logged in, 'log out' link and link to
    private page when they are.
  - Removed Mantissa/xmantissa/examples/autoapp.tac
    (superceded by "axiomatic start")
  - Fully-functional standalone development application ("axiomatic mantissa")
  - General preference inspection and configuration page added
  - Better support for anonymously viewed public pages
  - Support for multi-application search and search results aggregation
  - Skinned free-ticket-signup page
  - Lots of new docstrings
  - Administrative page for viewing unhandled exceptions which have occurred
    added
  - Experimental support for Nevow Athena-based fragments
