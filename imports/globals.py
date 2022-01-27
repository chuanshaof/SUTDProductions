def initialize():
    global WAIT_CODE, START, PROJECT_CONFIRM, REMOVE, ANNOUNCE_QUERY, ANNOUNCE, EDIT, EDIT_CONFIRM, VIEW_PROJECTS, \
        ADD, SUGGEST, SUGGEST_CONFIRM, PRESIDENT, project_details

    WAIT_CODE = range(1)
    START = range(1, 2)

    REMOVE = range(14, 15)
    ANNOUNCE_QUERY, ANNOUNCE = range(15, 17)
    EDIT, EDIT_CONFIRM = range(17, 19)
    VIEW_PROJECTS = range(19, 20)
    ADD, PROJECT_CONFIRM = range(20, 22)
    SUGGEST, SUGGEST_CONFIRM = range(22, 24)

    PRESIDENT = "kong_noah"

    project_details = ["Name:",
                       "Description:",
                       "POC:",
                       "Venue:",
                       "Project Purpose:",
                       "Inspiration:",
                       "Roles needed:",
                       "Production Deadline:",
                       "Project Requirement:",
                       "Team:"]

