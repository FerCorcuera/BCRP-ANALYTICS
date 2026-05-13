# Analytics on the Payment System in Peru

In this project we are investigating and applying different ML techniques to the Payment System data provided by the BCRP.

# Definitions

## Low value payment market by payment instrument

- `bajo_valor_cheques`: pagos realizados mediante cheques.
- `bajo_valor_tarjetas_pago`: pagos realizados con tarjetas de débito y crédito.
- `bajo_valor_transferencias_intrabancarias`: transferencias entre cuentas del mismo banco.
- `bajo_valor_transferencias_interbancarias`: transferencias entre diferentes entidades financieras.
- `bajo_valor_debitos_directos`: pagos autorizados previamente e iniciados por el beneficiario (PULL transactions).
- `bajo_valor_dinero_electronico`: dinero almacenado electrónicamente bajo esquemas prepago o billeteras electrónicas.


# Current Findings

1. Similar card payment series appear across multiple BCRP statistical groups because they represent different analytical perspectives of the payment system through history
2. Some older groups such as "High and Low Value Payments" likely correspond to previous methodologies used by the BCRP to structure the retail payment market.
3. An attempt was made to replicate the BCRP chart on low-value retail payment instruments
4. The main unresolved problem is identifying how the filtered "otros canales de tranfeencias interbancarias"
