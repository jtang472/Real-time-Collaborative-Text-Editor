# CS4459 Group Project Report

## Team Members:
- Eric Liu
- Jamie Tang
- Adrian Koziskie
- Modin Wang

## The Problem:
The problem tackled was live collaboration on a text document. Multiple users needed the ability to simultaneously edit a document, streamlining the writing process. Implementing a distributed system to solve this required ensuring a consistent state of the document for all users and efficiently handling data in potentially large documents. Challenges included concurrency issues and preventing conflict or data loss in document states.

## Our Project:
We created a real-time collaborative text editor using gRPC and WebSockets. To enhance responsiveness and performance, we implemented a piece table data structure, which updates the document efficiently in the database and reduces the size of messages between the client and server.

## Our Design:
### Initial Design:
- **Proto File**: Drafted to contain request messages for collaborative text editor actions (insert, delete, fetch).
- **Data Structure**: Selected a piece table to represent the changing document state, with two main components: the original document and a buffer for additions (inserts).
- **Function Messages**: Defined in the proto file to handle document state and piece tables.

### Server and Client Implementation:
- **Server Architecture**: Implemented functions from the proto file for document state manipulation using the piece table structure, enabling efficient insert, delete, and fetch operations. Connected to MongoDB for document storage and scheduled backup snapshots using APScheduler.
- **WebSockets**: Integrated for low-latency, real-time collaboration. Used Socket.IO for compatibility across browsers and fallback options.
- **User Interface**: Crafted using HTML, CSS, and JavaScript for dynamic integration and functionality.

### Version Control:
- **Repository**: Established on BitBucket with Git for version control.
- **Dependencies**: Managed via a `requirement.txt` file for quick installation in a Python virtual environment.

## Challenges:
### JavaScript Integration with gRPC:
- **Initial Hurdles**: Compiling the .proto file with JavaScript was complex.
- **Solution**: Utilized gRPC Web, enabling compilation of .proto files and connection to gRPC services via an Envoy-powered proxy.

### MongoDB Familiarity:
- **Learning Curve**: Team's unfamiliarity with MongoDB required learning resources and regular knowledge-sharing meetings.
- **Outcome**: Successfully integrated MongoDB with the application, gaining valuable technical skills.

### Dependency Management:
- **Setup Issues**: Connecting to the Bitbucket repository and setting up MongoDB on different operating systems were challenging.
- **Teamwork**: Collaborative efforts ensured all team members could set up the system, enabling smooth development.

