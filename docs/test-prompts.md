# Test Prompts for Claude Desktop

## Function Tools (ไม่ต้อง start mock server)

### convert_units
```
Use the convert_units tool to convert 100 kg to lb
```
```
Use the convert_units tool to convert 1 km to miles
```
```
Use the convert_units tool to convert 0 celsius to fahrenheit
```
```
Use the convert_units tool to convert 100 celsius to kelvin
```
```
ลองใช้ convert_units tool แปลง 180 ซม. เป็นฟุต
```

### compound_interest
```
Use the compound_interest tool with principal=100000, rate=0.05, years=5
```
```
Use the compound_interest tool: principal 500000, rate 0.03, years 10, compounding annually (n=1)
```
```
ใช้ compound_interest tool คำนวณ: เงินต้น 200,000 บาท ดอกเบี้ย 4% ต่อปี 3 ปี
```

---

## API Tools (ต้อง start mock server ก่อน: `uvicorn mock_server.server:app --port 8080`)

### calculate_statistics
```
Use the calculate_statistics tool with numbers [10, 25, 37, 42, 8, 99, 15, 60]
```
```
Use the calculate_statistics tool on these values: [100, 200, 150, 175, 225, 300, 125]
```

### amortize_loan
```
Use the amortize_loan tool: principal=3000000, annual_rate=0.0625, months=240
```
```
Use the amortize_loan tool: principal=500000, annual_rate=0.05, months=60
```

---

## Error Cases (ทดสอบ validation)

```
Use the convert_units tool to convert 10 km to kg
```
> Expected: error — cannot convert length to weight

```
Use the compound_interest tool with principal=10000, rate=0.05, years=3, n=0
```
> Expected: error — n must be at least 1

```
Use the amortize_loan tool: principal=0, annual_rate=0.05, months=12
```
> Expected: error — principal must be > 0
