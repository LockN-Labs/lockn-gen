# Linear GraphQL API Reference

## Authentication

Use the `LINEAR_API_KEY` environment variable:

```bash
export LINEAR_API_KEY=lin_api_YOUR_KEY
```

## Querying Issues

### Query by ID

```graphql
{
  issue(input: { id: "LOC-10" }) {
    id
    title
    description
    status
    labels {
      name
    }
    assignee {
      id
      name
    }
    createdAt
    updatedAt
  }
}
```

### List Issues in Project

```graphql
{
  project(input: { id: "PRJ_loc10" }) {
    issues(first: 20, filter: { status: { not: { name: "Done" } } }) {
      edges {
        node {
          id
          title
          status
          labels {
            name
          }
        }
      }
    }
  }
}
```

## Creating Issues

```graphql
mutation {
  createIssue(input: {
    title: "Implement QueryService"
    teamId: "TBD"
    description: "Add search query capabilities for receipts"
    labels: {
      create: ["agent:coder"]
    }
  }) {
    id
    title
    status
  }
}
```

## Creating Subtasks

Subtasks are just issues created within the same team:

```graphql
mutation {
  createIssue(input: {
    title: "Create AgentSession entity"
    parent: {
      create: {
        issueId: "LOC-7"
      }
    }
    teamId: "TBD"
    labels: {
      create: ["agent:coder"]
    }
  }) {
    id
    title
    status
  }
}
```

## Updating Issues

### Update Status

```graphql
mutation {
  updateIssue(input: {
    id: "LOC-7-1"
    status: "in-progress"
  }) {
    id
    title
    status
  }
}
```

### Update Assignee

```graphql
mutation {
  updateIssue(input: {
    id: "LOC-7-1"
    assignee: {
      set: "user_12345"
    }
  }) {
    id
    title
    assignee {
      id
      name
    }
  }
}
```

## Status Options

| Status | Description |
|--------|-------------|
| `backlog` | Not started, queued for work |
| `todo` | Ready to start |
| `in-progress` | Currently being worked on |
| `done` | Completed |
| `cancelled` | Work abandoned |

## Common Queries

### Get all pending subtasks for an issue

```graphql
{
  issue(input: { id: "LOC-10" }) {
    subtasks(first: 20, filter: { status: { not: { name: "Done" } } }) {
      edges {
        node {
          id
          title
          status
          labels {
            name
          }
        }
      }
    }
  }
}
```

### Get issues with specific label

```graphql
{
  issues(filter: {
    labels: {
      name: {
        eq: "agent:coder"
      }
    },
    status: {
      not: {
        name: "Done"
      }
    }
  }) {
    nodes {
      id
      title
      status
      assignee {
        name
      }
    }
  }
}
```

## Error Handling

Linear API errors include a `message` field:

```json
{
  "errors": [
    {
      "message": "Issue not found",
      "locations": [{ "line": 2, "column": 3 }],
      "path": ["issue"]
    }
  ]
}
```

Always check for `errors` in the response.
