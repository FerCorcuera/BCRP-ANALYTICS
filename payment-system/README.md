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

1. Similar payment series appear across multiple BCRP statistical groups because they represent different historical and methodological perspectives of the Peruvian payment system. This includes differences in series such as low-value payments (`PN39936SM` vs `PN42160EM`), likely due to methodological changes over time.

2. An attempt was made to replicate the BCRP chart on low-value retail payment instruments published in Revista Moneda N.° 201. The main unresolved issue is identifying how the BCRP filtered the category `"otros canales de transferencias intrabancarias"` to exclude canales-mayoristas operations.

3. The merchant acquiring and payment facilitator datasets appear to be constructed using MCC-based merchant segment aggregations defined by the BCRP. Segments such as pharmacies, gas stations, restaurants, supermarkets, transport and microbusinesses match directly with the official MCC classifications.

4. According to the BCRP methodology documentation, transactions related to financial institutions, government and public services are explicitly excluded from the published merchant aggregates. Remaining merchant categories not explicitly excluded are likely grouped inside `"otros segmentos"`. (see source 9)

5. The total card payment market is significantly larger than the published acquiring and payment facilitator market. This suggests that the acquiring/facilitator datasets do not represent the full card-processing ecosystem, but rather a specific subset of merchant acquiring activity reported under the BCRP framework.

6. The share of foreign-currency transactions inside the acquiring and facilitator ecosystem is relatively small compared to the broader low-value payment market. Therefore, using total transaction values (`MN + ME`) appears methodologically consistent for aggregate market analysis, while currency decomposition can still be performed separately when needed. 

7. Exploratory time-series analysis suggests that the acq and fac market is non stationary and shows trend and seasonal behavior. SARIMA and Prophet baseline models were able to capture some of these dynamics but the limited sample size (27 observations) introduces significant challenges, resulting in unstable or statistically weak coefficient estimates.

---
---
# Current Questions

1. Why is the total card payment market significantly larger than the published acquiring and payment facilitator market, despite card payments generally requiring merchant acquiring infrastructure?

2. How much of the immediate payment and wallet ecosystem corresponds to actual merchant commerce (P2B) versus person-to-person transfers (P2P)?

3. What exact methodology did the BCRP use to filter wholesale-related operations from `"otros canales de transferencias intrabancarias"` in the retail payment market publication?

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