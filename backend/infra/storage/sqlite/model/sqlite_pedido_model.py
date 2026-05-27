from backend.domain.entity.pedido import Pedido
from backend.domain.entity.pedido_item import PedidoItem

class SqlitePedidoModel:
    @staticmethod
    def to_entity(row) -> Pedido:
        """Converte uma linha bruta de Pedido em uma Entidade de Domínio Pedido"""
        if not row:
            return None
        return Pedido(
            id=row["Id"],
            usuario_id=row["UsuarioId"],
            status=row["Status"],
            criado_em=row["CriadoEm"],
            endereco_entrega=row.get("EnderecoEntrega"),
            forma_pagamento=row.get("FormaPagamento"),
            valor_frete=row.get("ValorFrete"),
            total_pago=row.get("TotalPago")
        )

class SqlitePedidoItemModel:
    @staticmethod
    def to_entity(row) -> PedidoItem:
        """Converte uma linha bruta de PedidoItem em uma Entidade de Domínio PedidoItem"""
        if not row:
            return None
        return PedidoItem(
            id=row["Id"],
            pedido_id=row["PedidoId"],
            item_nome=row["ItemNome"],
            item_foto=row["ItemFoto"],
            item_valor=row["ItemValor"],
            quantidade=row["Quantidade"],
            observacao=row["Observacao"],
            criado_em=row["CriadoEm"]
        )
