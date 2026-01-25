# REST and RESTful refresher.
REST stands for Representational State Transfer (architectural style), RESTful is the implementation.

## REST pilars:

1. Uniform interface: Standard formats for communication (representation). Derivated constrains:
>    1. Requests should identify resources. They do so by using a **uniform resource identifier** (URI).
>    2. Clients have enough information in the resource representation to modify or delete the resource if they want to. The server meets this condition by sending metadata that describes the resource further.
>    3. Clients receive information about how to process the representation further. The server achieves this by sending self-descriptive messages that contain metadata about how the client can best use them.
>    4. Clients receive information about all other related resources they need to complete a task. The server achieves this by sending hyperlinks in the representation so that clients can dynamically discover more resources.

2. Statelessness: server completes every client request independently of all previous requests.
3. Layered system: client shoudln't know if is conencted to the server or an intermediary.
4. Cacheability: responses should be marked as cacheable or not.
5. Code on demand: you can send code to be executed by the client.
## Request components

1. URI: For REST services, the server typically performs resource identification by using a Uniform Resource Locator (URL).
2. Method: HTTP methods GET/POST/PUT/DELETE.
3. Headers: metadata exchange:
    - Data for POST, PUT
    - Parameters: Path, Query and Cookies.

## Authentication Methods

1. Basic authentication: User/Password as part of the request header.
2. Bearer authentication: Passing the token from a previous login.
3. API Keys: Server generates key value that identify users. Less secure as they transmit the key.
4. OAuth: The server first requests a password and then asks for an additional token to complete the authorization process.

## Response components

1. Status line: 2XX/3XX/4XX/5XX
2. Message body: Resource representation, on XML or JSON format.
3. Headers: They give more context about the response and include information such as the server, encoding, date, and content type.

## Documentation

1. [AWS Documentation](https://aws.amazon.com/what-is/restful-api/)
2. [Microsoft Best Practices](https://learn.microsoft.com/en-us/azure/architecture/best-practices/api-design)