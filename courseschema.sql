-- Table for storing courses
CREATE TABLE courses (
    id SERIAL PRIMARY KEY,   -- Unique identifier for each course
    name VARCHAR(255) NOT NULL -- Course name
);

-- Table for storing reviews
CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,        -- Unique identifier for each review
    course_id INT NOT NULL,       -- Foreign key for the course
    title VARCHAR(255) NOT NULL,  -- Title of the review
    content TEXT NOT NULL,        -- Review content
    score INT CHECK (score BETWEEN 0 AND 10), -- Score between 0 and 10
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Review creation date
    FOREIGN KEY (course_id) REFERENCES courses(id) -- Link reviews to courses
);
