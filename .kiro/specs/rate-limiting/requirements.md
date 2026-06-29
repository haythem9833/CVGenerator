# Requirements Document

## Introduction

The CV Generator application requires a rate limiting feature to prevent abuse and ensure fair usage across all users. This feature will limit the number of CV generations each user can perform within a 24-hour period using database-level tracking for persistence and reliability.

## Glossary

- **Rate_Limiter**: The system component responsible for enforcing generation limits
- **Generation_Counter**: The database-tracked count of CV generations per user
- **Daily_Limit**: The maximum number of CV generations allowed per user in a 24-hour period
- **Rate_Limit_Window**: A 24-hour period starting from the user's first generation of the day
- **User**: An authenticated individual identified by their user_id from the JWT token
- **CV_Generation_Request**: An API request to create a new CV document
- **Rate_Limit_Record**: A database record tracking generation count and window start time for a user

## Requirements

### Requirement 1: Track Generation Count

**User Story:** As the system, I want to track the number of CV generations per user in the database, so that limits persist across sessions and server restarts.

#### Acceptance Criteria

1. WHEN a User submits a CV_Generation_Request, THE Rate_Limiter SHALL increment the Generation_Counter in the database for that User
2. WHEN a User submits their first CV_Generation_Request of a new day, THE Rate_Limiter SHALL create a new Rate_Limit_Record with Generation_Counter set to 1 and the current timestamp
3. THE Rate_Limiter SHALL store the Rate_Limit_Record with the user_id, Generation_Counter, and Rate_Limit_Window start timestamp
4. WHEN retrieving a Rate_Limit_Record, THE Rate_Limiter SHALL return the current Generation_Counter and Rate_Limit_Window start time

### Requirement 2: Enforce Daily Limit

**User Story:** As a system administrator, I want to limit CV generations per user per day, so that system resources are distributed fairly and abuse is prevented.

#### Acceptance Criteria

1. THE Rate_Limiter SHALL enforce a Daily_Limit of CV generations per User within a 24-hour period
2. WHEN a User submits a CV_Generation_Request and the Generation_Counter is less than the Daily_Limit, THE Rate_Limiter SHALL allow the request to proceed
3. WHEN a User submits a CV_Generation_Request and the Generation_Counter equals or exceeds the Daily_Limit, THE Rate_Limiter SHALL reject the request
4. WHEN the Rate_Limiter rejects a request, THE Rate_Limiter SHALL return an HTTP 429 status code
5. THE Rate_Limiter SHALL make the Daily_Limit configurable through application configuration

### Requirement 3: Reset Rate Limit Window

**User Story:** As a user, I want my generation limit to reset after 24 hours, so that I can continue using the service each day.

#### Acceptance Criteria

1. WHEN a User submits a CV_Generation_Request and more than 24 hours have passed since the Rate_Limit_Window start time, THE Rate_Limiter SHALL reset the Generation_Counter to 1 and update the Rate_Limit_Window start time to the current timestamp
2. WHEN a User submits a CV_Generation_Request and less than 24 hours have passed since the Rate_Limit_Window start time, THE Rate_Limiter SHALL increment the existing Generation_Counter
3. THE Rate_Limiter SHALL calculate the 24-hour period from the Rate_Limit_Window start time stored in the database

### Requirement 4: Provide Rate Limit Information

**User Story:** As a user, I want to know my current usage and when my limit resets, so that I can plan my CV generations accordingly.

#### Acceptance Criteria

1. WHEN a User submits a CV_Generation_Request, THE Rate_Limiter SHALL include rate limit information in the response headers
2. THE Rate_Limiter SHALL include the Daily_Limit value in the response header X-RateLimit-Limit
3. THE Rate_Limiter SHALL include the remaining generations in the response header X-RateLimit-Remaining
4. THE Rate_Limiter SHALL include the Rate_Limit_Window reset timestamp in the response header X-RateLimit-Reset
5. WHEN the Rate_Limiter rejects a request, THE Rate_Limiter SHALL include a Retry-After header with seconds until the window resets

### Requirement 5: Handle Rate Limit Errors

**User Story:** As a user, I want to receive clear error messages when I exceed my rate limit, so that I understand why my request was rejected and when I can try again.

#### Acceptance Criteria

1. WHEN the Rate_Limiter rejects a CV_Generation_Request due to exceeding the Daily_Limit, THE Rate_Limiter SHALL return a JSON error response
2. THE Rate_Limiter SHALL include an error message stating that the daily limit has been exceeded
3. THE Rate_Limiter SHALL include the Daily_Limit value in the error response
4. THE Rate_Limiter SHALL include the time remaining until the Rate_Limit_Window resets in the error response
5. THE Rate_Limiter SHALL include the reset timestamp in ISO 8601 format in the error response

### Requirement 6: Authenticate Before Rate Limiting

**User Story:** As the system, I want to verify user authentication before applying rate limits, so that only valid users are tracked and anonymous requests are handled separately.

#### Acceptance Criteria

1. WHEN a CV_Generation_Request is received without a valid JWT token, THE Rate_Limiter SHALL not apply rate limiting
2. WHEN a CV_Generation_Request is received without a valid JWT token, THE API SHALL return an HTTP 401 status code with an authentication error
3. WHEN a CV_Generation_Request is received with a valid JWT token, THE Rate_Limiter SHALL extract the user_id from the token
4. THE Rate_Limiter SHALL apply rate limiting only after successful authentication

### Requirement 7: Handle Concurrent Requests

**User Story:** As the system, I want to handle concurrent CV generation requests from the same user correctly, so that race conditions do not allow users to exceed their rate limits.

#### Acceptance Criteria

1. WHEN multiple CV_Generation_Requests from the same User arrive concurrently, THE Rate_Limiter SHALL ensure the Generation_Counter is incremented atomically
2. WHEN multiple CV_Generation_Requests from the same User arrive concurrently and would collectively exceed the Daily_Limit, THE Rate_Limiter SHALL reject all requests that would exceed the limit
3. THE Rate_Limiter SHALL use database-level atomic operations or row-level locking to prevent race conditions

### Requirement 8: Database Schema for Rate Limiting

**User Story:** As a developer, I want a proper database schema for rate limiting, so that the system can efficiently store and query rate limit data.

#### Acceptance Criteria

1. THE Rate_Limiter SHALL use a database table named rate_limits to store Rate_Limit_Records
2. THE rate_limits table SHALL contain a user_id column as the primary key referencing the users table
3. THE rate_limits table SHALL contain a generation_count column storing the current Generation_Counter as an integer
4. THE rate_limits table SHALL contain a window_start column storing the Rate_Limit_Window start time as a timestamp with timezone
5. THE rate_limits table SHALL contain an updated_at column storing the last update timestamp with timezone
