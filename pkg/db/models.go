package db

import (
	"database/sql/driver"
	"encoding/json"
	"errors"
	"time"

	"github.com/jinzhu/gorm"
	"github.com/jinzhu/gorm/dialects/postgres"
	"github.com/lib/pq"
)

type Metadata map[string]string

func (a Metadata) Value() (driver.Value, error) {
	return json.Marshal(a)
}

func (a *Metadata) Scan(value interface{}) error {
	b, ok := value.([]byte)
	if !ok {
		return errors.New("type assertion to []byte failed")
	}
	return json.Unmarshal(b, &a)
}

type Campaign struct {
	gorm.Model
	CreatedBy        string //take it or leave it really meh
	NotBefore        time.Time
	NotAfter         time.Time
	ScheduleInterval time.Duration
	Users            pq.StringArray `gorm:"type:varchar(255)[]"`
	Passwords        pq.StringArray `gorm:"type:varchar(255)[]"`
	Provider         string
	ProviderMetadata postgres.Jsonb
}

type Task struct {
	// NotBefore will prevent execution until this time
	NotBefore time.Time `json:"not_before"`

	// NotAfter will prevent execution after this time
	NotAfter time.Time `json:"not_after"`

	// Username is the username at the identity provider
	Username string `json:"username"`

	// Password is the password to guess against the identity provider
	Password string `json:"password"`

	// Provider is the name of identity provider, used to look up the right nozzle
	Provider string `json:"provider"`

	// ProviderMetadata is any required configuration data for the provider
	ProviderMetadata map[string]string `json:"metadata"`
}

func (t *Task) MarshalBinary() (data []byte, err error) {
	return json.Marshal(t)
}

func (t *Task) UnmarshalBinary(data []byte) error {
	return json.Unmarshal(data, &t)
}
