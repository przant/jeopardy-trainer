# Gopardy Question Bank - MVP

## Q001 [basic] [multiple-choice]
**Question:** What's the zero value of a string in Go?

**Options:**
A) null
B) ""
C) nil
D) undefined

**Answer:** B
**Explanation:** Go initializes strings to empty string (""), not nil. Only pointers, slices, maps, channels, and interfaces have nil as zero value.

---

## Q002 [basic] [fill-blank]
**Question:** Complete the command to download dependencies:

```bash
go mod ________
```

**Answer:** download
**Explanation:** `go mod download` fetches dependencies listed in go.mod into the module cache. Use `go mod tidy` to add/remove dependencies based on actual imports.

---

## Q003 [basic] [multiple-choice]
**Question:** Which command builds a static binary for Linux?

**Options:**
A) go build -static -o app
B) CGO_ENABLED=0 GOOS=linux go build -o app
C) go build --no-cgo -o app
D) STATIC=1 go build -o app

**Answer:** B
**Explanation:** CGO_ENABLED=0 disables cgo (no C dependencies), GOOS=linux sets target OS. Required for Alpine/scratch Docker images.

---

## Q004 [basic] [fill-blank]
**Question:** What package provides HTTP server functionality?

```go
import "___/___"
```

**Answer:** net/http
**Explanation:** Standard library package `net/http` provides HTTP client and server implementations. No external framework needed for basic APIs.

---

## Q005 [basic] [multiple-choice]
**Question:** What's the correct HTTP handler signature?

**Options:**
A) func(r *http.Request) http.Response
B) func(w http.ResponseWriter, r *http.Request)
C) func(req, res http.Context)
D) func(http.Request) (http.Response, error)

**Answer:** B
**Explanation:** Handlers receive ResponseWriter (for writing response) and pointer to Request. Standard signature: `func(w http.ResponseWriter, r *http.Request)`.

---

## Q006 [intermediate] [multiple-choice]
**Question:** This code has a race condition. Why?

```go
var counter int
for i := 0; i < 100; i++ {
    go func() {
        counter++
    }()
}
```

**Options:**
A) Missing WaitGroup
B) Multiple goroutines modifying shared variable without synchronization
C) counter should be int64
D) Need buffered channel

**Answer:** B
**Explanation:** Multiple goroutines incrementing counter creates a race condition. Fix with mutex, atomic operations, or channels. The missing WaitGroup is also a problem but not the race condition.

---

## Q007 [intermediate] [fill-blank]
**Question:** Complete the error wrapping syntax:

```go
return fmt.Errorf("failed to process: %__, err)
```

**Answer:** w
**Explanation:** `%w` wraps the error, allowing errors.Is() and errors.As() to unwrap the chain. Use `%v` for string representation without wrapping.

---

## Q008 [basic] [multiple-choice]
**Question:** How do you check if an error matches a sentinel error?

**Options:**
A) if err == ErrNotFound
B) if err.Error() == "not found"
C) if errors.Is(err, ErrNotFound)
D) if strings.Contains(err.Error(), "not found")

**Answer:** C
**Explanation:** errors.Is() unwraps the error chain to check. Direct comparison (==) fails if error is wrapped with fmt.Errorf("%w").

---

## Q009 [intermediate] [multiple-choice]
**Question:** What's the difference between `Lock()` and `RLock()`?

**Options:**
A) Lock() is for reading, RLock() is for writing
B) Lock() is exclusive, RLock() allows multiple readers
C) Lock() is faster than RLock()
D) No difference, just aliases

**Answer:** B
**Explanation:** RLock() allows multiple concurrent readers. Lock() is exclusive (no readers or writers). Use RLock() for read operations, Lock() for writes.

---

## Q010 [basic] [fill-blank]
**Question:** Complete the context creation with 5-second timeout:

```go
ctx, cancel := context.________(context.Background(), 5*time.Second)
defer cancel()
```

**Answer:** WithTimeout
**Explanation:** WithTimeout creates a context that cancels after duration. Always defer cancel() to release resources even if timeout doesn't fire.

---

## Q011 [gotcha] [multiple-choice]
**Question:** What's wrong with this code?

```go
func HandleGet(w http.ResponseWriter, r *http.Request) {
    w.Write([]byte("Hello"))
    w.WriteHeader(http.StatusOK)
}
```

**Options:**
A) Nothing wrong
B) WriteHeader must come before Write
C) Missing Content-Type header
D) Should use fmt.Fprintf instead

**Answer:** B
**Explanation:** Write() implicitly sends status 200 if WriteHeader() hasn't been called. Calling WriteHeader() after Write() does nothing. Order matters: headers before body.

---

## Q012 [intermediate] [multiple-choice]
**Question:** Why use `defer` with mutex operations?

**Options:**
A) Performance optimization
B) Guarantees unlock even if function panics or returns early
C) Required by Go syntax
D) Improves readability only

**Answer:** B
**Explanation:** defer ensures unlock happens regardless of how function exits (return, panic, etc.). Critical for avoiding deadlocks.

---

## Q013 [basic] [fill-blank]
**Question:** What JSON struct tag makes a field optional during unmarshaling?

```go
type User struct {
    Name string `json:"name,________"`
}
```

**Answer:** omitempty
**Explanation:** `omitempty` excludes the field from JSON output if it has zero value. For input, all fields are already optional unless you validate manually.

---

## Q014 [intermediate] [multiple-choice]
**Question:** How do you decode JSON from request body?

**Options:**
A) json.Unmarshal(r.Body, &user)
B) json.NewDecoder(r.Body).Decode(&user)
C) json.Parse(r.Body, &user)
D) user.FromJSON(r.Body)

**Answer:** B
**Explanation:** json.NewDecoder reads from io.Reader (r.Body) efficiently. json.Unmarshal requires []byte, less efficient for streams.

---

## Q015 [gotcha] [multiple-choice]
**Question:** This goroutine leaks. Why?

```go
for _, user := range users {
    go func() {
        process(user)
    }()
}
```

**Options:**
A) Missing WaitGroup
B) All goroutines process the last user (closure bug)
C) Should use buffered channel
D) process() might panic

**Answer:** B
**Explanation:** Classic closure bug. All goroutines capture same `user` variable reference. By loop end, `user` is last value. Fix: `go func(u User) { process(u) }(user)`.

---

## Q016 [basic] [multiple-choice]
**Question:** What's the correct way to create a slice with capacity 10?

**Options:**
A) slice := []int{10}
B) slice := make([]int, 10)
C) slice := make([]int, 0, 10)
D) slice := new([]int, 10)

**Answer:** C
**Explanation:** `make([]int, 0, 10)` creates slice with length 0, capacity 10. Option B creates length 10 (10 zero values). Option A is array literal with one element.

---

## Q017 [intermediate] [fill-blank]
**Question:** Complete the table-driven test pattern:

```go
tests := []struct {
    name string
    input int
    want int
}{
    {"positive", 5, 10},
}
for _, tt := range tests {
    t._____(tt.name, func(t *testing.T) {
        // test code
    })
}
```

**Answer:** Run
**Explanation:** t.Run() creates subtests, allowing parallel execution and better failure reporting. Each subtest gets its own name.

---

## Q018 [basic] [multiple-choice]
**Question:** How do you get a query parameter from URL?

**Options:**
A) r.QueryParam("id")
B) r.URL.Query().Get("id")
C) r.GetParam("id")
D) r.Params["id"]

**Answer:** B
**Explanation:** r.URL.Query() returns url.Values (map[string][]string), then Get("id") retrieves first value. For multiple values, use Query()["id"].

---

## Q019 [gotcha] [multiple-choice]
**Question:** What's the output?

```go
defer fmt.Println("1")
defer fmt.Println("2")
defer fmt.Println("3")
```

**Options:**
A) 1 2 3
B) 3 2 1
C) Random order
D) Compile error

**Answer:** B
**Explanation:** Defers execute in LIFO order (stack). Last defer registered runs first. Output: 3, 2, 1.

---

## Q020 [intermediate] [multiple-choice]
**Question:** Why use pointer receiver for this method?

```go
func (u *User) SetName(name string) {
    u.Name = name
}
```

**Options:**
A) Performance only
B) Method modifies the receiver
C) Required for exported methods
D) All methods must use pointer receivers

**Answer:** B
**Explanation:** Pointer receiver allows modifying the actual struct. Value receiver would modify a copy. Also use pointers for large structs (avoid copying) and consistency.

---

## Q021 [basic] [fill-blank]
**Question:** What package handles PostgreSQL connections?

```go
import "github.com/jackc/___/v5"
```

**Answer:** pgx
**Explanation:** pgx is the modern, pure Go PostgreSQL driver. Alternatives: lib/pq (older), pgx with database/sql interface.

---

## Q022 [intermediate] [multiple-choice]
**Question:** What's wrong with this connection pool?

```go
pool, err := pgxpool.New(ctx, dbURL)
if err != nil {
    log.Fatal(err)
}
// ... use pool ...
```

**Options:**
A) Missing pool.Close()
B) Should use Connect() not New()
C) Missing defer pool.Close()
D) Nothing wrong

**Answer:** C
**Explanation:** Always close the pool to release connections. Use defer pool.Close() at function start. Missing this leaks database connections.

---

## Q023 [gotcha] [multiple-choice]
**Question:** This query is vulnerable. To what?

```go
query := fmt.Sprintf("SELECT * FROM users WHERE id = '%s'", id)
db.Query(ctx, query)
```

**Options:**
A) SQL injection
B) Memory leak
C) Race condition
D) Context timeout

**Answer:** A
**Explanation:** Never use string formatting for SQL. Malicious `id` like `1' OR '1'='1` bypasses auth. Use parameterized queries: `db.Query(ctx, "SELECT * FROM users WHERE id = $1", id)`.

---

## Q024 [intermediate] [multiple-choice]
**Question:** What does pgx.ErrNoRows indicate?

**Options:**
A) Database connection failed
B) Query syntax error
C) Query returned zero rows
D) Permission denied

**Answer:** C
**Explanation:** QueryRow().Scan() returns pgx.ErrNoRows when no rows match. Not an error - just means "not found". Common pattern: `if errors.Is(err, pgx.ErrNoRows) { return ErrNotFound }`.

---

## Q025 [basic] [fill-blank]
**Question:** Complete the HTTP status code for resource created:

```go
w.WriteHeader(http.Status______)
```

**Answer:** Created
**Explanation:** http.StatusCreated is 201. Use after POST creates new resource. Other common codes: 200 OK, 400 BadRequest, 404 NotFound, 500 InternalServerError.

---

## Q026 [intermediate] [multiple-choice]
**Question:** When should you use a channel instead of a mutex?

**Options:**
A) Protecting a simple counter
B) Passing data between goroutines
C) Protecting a map
D) Never, mutexes are always better

**Answer:** B
**Explanation:** Channels for communication/coordination, mutexes for protecting shared state. "Share memory by communicating" (channels) vs "protect shared memory" (mutexes).

---

## Q027 [basic] [multiple-choice]
**Question:** What's the idiomatic way to name a constructor function?

**Options:**
A) CreateUser()
B) user.New()
C) NewUser()
D) UserConstructor()

**Answer:** C
**Explanation:** Go convention: `NewType()` or `New()` in package. Example: `http.NewRequest()`, `pgxpool.New()`. Returns pointer if type is struct: `func NewUser() *User`.

---

## Q028 [gotcha] [multiple-choice]
**Question:** Why does this test fail intermittently?

```go
func TestConcurrent(t *testing.T) {
    counter := 0
    for i := 0; i < 100; i++ {
        go func() {
            counter++
        }()
    }
    time.Sleep(time.Second)
    if counter != 100 {
        t.Fail()
    }
}
```

**Options:**
A) Sleep duration too short
B) Race condition on counter variable
C) Missing t.Parallel()
D) Should use testing.B not testing.T

**Answer:** B
**Explanation:** Multiple goroutines increment counter without synchronization. Data race. Sleep doesn't fix race conditions. Use sync.Mutex, atomic, or channel. Run `go test -race` to detect.

---

## Q029 [intermediate] [fill-blank]
**Question:** Complete the SELECT query with parameter placeholder:

```go
db.QueryRow(ctx, "SELECT name FROM users WHERE id = __", id)
```

**Answer:** $1
**Explanation:** PostgreSQL uses $1, $2, $3 for parameters (not ? like MySQL). Prevents SQL injection and allows query plan caching.

---

## Q030 [intermediate] [multiple-choice]
**Question:** What's the purpose of context.Background()?

**Options:**
A) Creates background goroutine
B) Root context with no deadline or cancellation
C) Timeout context with 30-second default
D) Context for HTTP requests only

**Answer:** B
**Explanation:** context.Background() is the root of context trees. Use at program start, main(), or when you don't have a parent context. Alternative: context.TODO() when unsure which context to use.