package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type Config struct {
	items map[string]string
}

func NewConfig(args []string) (*Config, error) {
	if len(args) != 1 {
		return nil, fmt.Errorf("new config error: %s", strings.Join(args, " "))
	}

	configPath := args[0]

	f, err := os.Open(configPath)
	if err != nil {
		return nil, fmt.Errorf("new config error: %w", err)
	}
	defer f.Close()

	sc := bufio.NewScanner(f)

	items := map[string]string{}

	for sc.Scan() {
		line := sc.Text()
		key, value, err := parseConfigLine(line)
		if err != nil {
			return nil, fmt.Errorf("new config error: %w", err)
		}
		items[key] = value
	}
	if sc.Err() != nil {
		return nil, fmt.Errorf("new config error: %w", err)
	}

	return &Config{items}, nil
}

func parseConfigLine(line string) (key, val string, err error) {
	keyValue := strings.Split(line, "=")
	if len(keyValue) != 2 {
		err = fmt.Errorf("parse config line error: %q", line)
		return
	}
	key = keyValue[0]
	val = keyValue[1]
	return
}

func (c *Config) Get(key string) (val string, err error) {
	val, ok := c.items[key]
	if !ok {
		err = fmt.Errorf("config key not found: %q", key)
		return
	}
	return
}

func (c *Config) GetAsInt(key string) (val int, err error) {
	s, err := c.Get(key)
	if err != nil {
		err = fmt.Errorf("config get as int error: %w", err)
		return
	}
	val, err = strconv.Atoi(s)
	if err != nil {
		err = fmt.Errorf("config get as int error: %w", err)
		return
	}
	return
}

func (c *Config) GetAsFloat64(key string) (val float64, err error) {
	s, err := c.Get(key)
	if err != nil {
		err = fmt.Errorf("config get as float64 error: %w", err)
		return
	}
	val, err = strconv.ParseFloat(s, 64)
	if err != nil {
		err = fmt.Errorf("config get as float64 error: %w", err)
		return
	}
	return
}
