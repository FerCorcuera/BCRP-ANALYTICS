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

1. Similar card payment series appear across multiple BCRP statistical groups because they represent different analytical perspectives of the payment system through history.

2. We can find differences in the same series but in different groups, like in the amounts of "Monto de bajo valor" (PN39936SM vs PN42160EM).

3. That could be because some older groups such as "Pagos de alto y bajo valor" likely correspond to previous methodologies used by the BCRP to structure the retail payment market.

4. An attempt was made to replicate the BCRP chart on low-value retail payment instruments.

5. The main unresolved problem is identifying how the filtered "otros canales de transferencias intrabancarias" were constructed in the BCRP publication.

6. The merchant acquiring and payment facilitator datasets appear to be constructed using MCC-based segment aggregations defined by the BCRP.

7. Segments such as pharmacies, gas stations, restaurants, supermarkets, transport and microbusinesses match directly with the MCC segment definitions published by the BCRP.

8. According to the BCRP methodology documentation, the segments related to financial institutions, government and public services are explicitly excluded from the published aggregates.

9. All remaining MCC categories that are not explicitly excluded are likely grouped inside "otros segmentos".

---
# Current questions:

1. What are the channels that QR payments made through adquirentes y facilitadores use?
---
# References and Documentation

1. [Payment Systems in Economy - Present and Future Tendencies](https://www.sciencedirect.com/science/article/pii/S187704281201169X?ref=pdf_download&fr=RR-2&rr=9fb2f9710c023c1b)

2. [Reporte del Sistema Nacional de Pagos - Marzo 2026](https://www.bcrp.gob.pe/docs/Publicaciones/reporte-del-sistema-nacional-de-pagos/2026/marzo/rspf-marzo-2026.pdf)

3. [Moneda 182 - Sistemas de Pago](https://www.bcrp.gob.pe/docs/Publicaciones/Revista-Moneda/moneda-182/moneda-182-08.pdf)

4. [Moneda 189 - Sistema de Pagos en el Perú](https://www.bcrp.gob.pe/docs/Publicaciones/Revista-Moneda/moneda-189/moneda-189-03.pdf)

5. [Moneda 201 - Factores de éxito de las billeteras digitales en el Perú y el rol del Banco Central](https://www.bcrp.gob.pe/docs/Publicaciones/Revista-Moneda/moneda-201/moneda-201-02.pdf)

6. [Moneda 202 - Avances en la fase 3 de interoperabilidad](https://www.bcrp.gob.pe/docs/Publicaciones/Revista-Moneda/moneda-202/moneda-202-04.pdf)

7. [Guía Metodológica BCRP 2025 - Sistemas de Pago](https://www.bcrp.gob.pe/docs/Publicaciones/Guia-Metodologica/2025/guia-metodologica-2025-04.pdf)

8. [Circular BCRP 0027-2022 - Interoperabilidad y anexos](https://www.bcrp.gob.pe/docs/Transparencia/Normas-Legales/Circulares/2022/circular-0027-2022-bcrp-anexos.pdf)

9. [Cuadros estadisticos 2026](https://www.bcrp.gob.pe/docs/Estadisticas/Cuadros-Estadisticos/2026/cuadros-estadisticos-16-2026.pdf)
---