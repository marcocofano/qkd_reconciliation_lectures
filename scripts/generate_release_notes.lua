-- Lua script to generate release notes without external dependencies

local changelog_path = "CHANGELOG.md"
local tag_to_release = arg[1] -- The tag we want to release (passed as CLI argument)
local repo_url = "https://github.com/marcocofano/qkd_reconciliation_lectures"
local header_emojis = {
    Added = "✨",
    Changed = "🔧",
    Fixed = "🐛",
    Removed = "🔥",
}

-- Read the changelog and extract the section for a specific tag
local function extract_changelog_section(tag)
    local file = io.open(changelog_path, "r")
    if not file then
        error("Failed to open " .. changelog_path)
    end

    local changelog_section = {}
    local in_section = false

    for line in file:lines() do
        if line:find("^## %[" .. tag:gsub("%.", "%%.") .. "%]") then
            in_section = true
        elseif in_section and line:find("^## %[%w") then
            -- End of the section for the tag
            break
        end

        if in_section then
            -- Add emojis to section headers
            for header, emoji in pairs(header_emojis) do
                line = line:gsub("^" .. header, emoji .. " " .. header)
            end
            table.insert(changelog_section, line)
        end
    end

    file:close()
    return table.concat(changelog_section, "\n")
end

-- Get all tags in the repository (sorted)
local function get_git_tags()
    local handle = io.popen("git tag --sort=-v:refname")
    if not handle then
        error("Failed to fetch git tags.")
    end

    local tags = handle:read("*a")
    handle:close()

    local tag_list = {}
    for tag in tags:gmatch("[^\n]+") do
        table.insert(tag_list, tag)
    end

    return tag_list
end

local function get_commits_between_tags(current_tag, previous_tag)
    -- If current_tag is nil, default to HEAD
    current_tag = current_tag or "HEAD"

    -- If previous_tag is nil, find the first commit
    if not previous_tag then
        local first_commit_cmd = "git rev-list --max-parents=0 HEAD"
        local first_commit_handle = io.popen(first_commit_cmd)
        if first_commit_handle then
            previous_tag = first_commit_handle:read("*l")
            first_commit_handle:close()
        end
    end
    local cmd = string.format("git log --pretty=format:'%%h %%s' %s...%s", previous_tag, current_tag)
    local handle = io.popen(cmd)
    if not handle then
        error("Failed to fetch commits.")
    end

    local commits = {}
    for line in handle:lines() do
        local short_hash, message = line:match("^(%S+)%s+(.+)$")
        if short_hash and message then
            local commit_link = string.format("[%s](%s/commit/%s)", short_hash, repo_url, short_hash)
            table.insert(commits, string.format("%s %s\n", commit_link, message))
        end
    end
    handle:close()

    return table.concat(commits, "")
end

-- Main script logic
local function main()
    if not tag_to_release then
        error("Usage: lua release_notes.lua <tag>")
    end

    local changelog_section = extract_changelog_section(tag_to_release)

    -- -- Get the tags from Git
    local tags = get_git_tags()
    local current_index = 0
    for i, current_tag in ipairs(tags) do
        if current_tag == tag_to_release then
            current_index = i
            break
        end
        current_tag = nil
    end

    local previous_tag = nil
    if current_index then
        previous_tag = tags[current_index + 1]
    end


    local commits = get_commits_between_tags(tag_to_release, previous_tag)
    --
    -- Generate the release notes
    local release_notes = {}
    table.insert(release_notes, "## Release Notes for " .. tag_to_release)
    table.insert(release_notes, changelog_section)
    table.insert(release_notes, "\n### Commits")
    table.insert(release_notes, commits)

    print(table.concat(release_notes, "\n"))
end

main()
