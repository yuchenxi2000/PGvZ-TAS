// 当前关卡的地形草稿；绘制操作只改本地数据，apply 才提交一次性动作。
window.PGvZTerrain = (() => {
    const types = [
        { value: 'Grass', label: '草地', en: 'Grass', short: '草', code: 'G' },
        { value: 'Dirt', label: '裸地', en: 'Dirt', short: '土', code: 'D' },
        { value: 'Pool', label: '泳池', en: 'Pool', short: '水', code: 'P' },
        { value: 'HighGround', label: '高地', en: 'High Ground', short: '高', code: 'H' },
        { value: 'Shallow', label: '浅水', en: 'Shallow Water', short: '浅', code: 'S' },
    ];
    function create({ sendAction }) {
        const { ref, computed } = Vue;
        const defaultDraft = () => ({
            background: 'Num1Day',
            grid: Array.from({ length: 6 }, (_, row) => Array(9).fill(row === 5 ? 'Dirt' : 'Grass')),
            rows: ['Normal', 'Normal', 'Normal', 'Normal', 'Normal', 'Dirt'],
        });
        const draft = ref(defaultDraft());
        const loading = ref(false);
        const applying = ref(false);
        const brush = ref('Grass');
        const selection = ref(null);
        const baseline = ref(JSON.stringify(draft.value));
        const busy = computed(() => loading.value || applying.value);
        const dirty = computed(() => JSON.stringify(draft.value) !== baseline.value);
        const clone = value => JSON.parse(JSON.stringify(value));

        function reset() {
            draft.value = defaultDraft();
            loading.value = false;
            applying.value = false;
            selection.value = null;
            baseline.value = JSON.stringify(draft.value);
        }
        function load() {
            if (busy.value) return;
            selection.value = null;
            loading.value = true;
            if (!sendAction('getTerrain')) loading.value = false;
        }
        function apply() {
            if (busy.value || selection.value) return;
            applying.value = true;
            if (!sendAction('applyTerrain', clone(draft.value))) applying.value = false;
        }
        function receive(result) {
            if (!['getTerrain', 'applyTerrain'].includes(result.name)) return;
            loading.value = false;
            applying.value = false;
            selection.value = null;
            if (result.ok) {
                draft.value = clone(result.value);
                baseline.value = JSON.stringify(draft.value);
            }
        }
        function paint(kind, row, col) {
            if (busy.value) return;
            if (kind === 'grid') draft.value.grid[row][col] = brush.value;
            else draft.value.rows[row] = brush.value === 'Grass' ? 'Normal' : brush.value;
        }
        function point(event, requireCell = false) {
            const grid = event.currentTarget.querySelector('.terrain-grid').getBoundingClientRect();
            const rows = event.currentTarget.querySelector('.terrain-rows').getBoundingClientRect();
            const inside = rect => event.clientX >= rect.left && event.clientX < rect.right
                && event.clientY >= rect.top && event.clientY < rect.bottom;
            if (requireCell && !inside(grid) && !inside(rows)) return null;
            // 0..8 是格子列，9 是行类型；间隔使用半列，避免尚未拖到另一侧就选中它。
            const col = event.clientX >= rows.left ? 9 : event.clientX >= grid.right ? 8.5
                : Math.max(0, Math.min(8, Math.floor((event.clientX - grid.left) / grid.width * 9)));
            return {
                row: Math.max(0, Math.min(5, Math.floor((event.clientY - grid.top) / grid.height * 6))),
                col,
            };
        }
        function pointerDown(event) {
            if (busy.value || selection.value || event.isPrimary === false || event.button !== 0) return;
            const cell = point(event, true);
            if (!cell) return;
            event.preventDefault();
            selection.value = { pointerId: event.pointerId, start: cell, end: cell };
            event.currentTarget.setPointerCapture(event.pointerId);
        }
        function pointerMove(event) {
            if (selection.value?.pointerId !== event.pointerId) return;
            selection.value.end = point(event);
        }
        function selected(kind, row, col) {
            const s = selection.value;
            const column = kind === 'rows' ? 9 : col;
            return Boolean(s
                && row >= Math.min(s.start.row, s.end.row) && row <= Math.max(s.start.row, s.end.row)
                && column >= Math.min(s.start.col, s.end.col) && column <= Math.max(s.start.col, s.end.col));
        }
        function pointerUp(event) {
            if (selection.value?.pointerId !== event.pointerId) return;
            pointerMove(event);
            for (let row = 0; row < 6; row++) {
                for (let col = 0; col < 10; col++) {
                    const kind = col === 9 ? 'rows' : 'grid';
                    if (selected(kind, row, col)) paint(kind, row, col);
                }
            }
            selection.value = null;
            event.currentTarget.releasePointerCapture(event.pointerId);
        }
        function cancel() { selection.value = null; }
        function cellClick(event, kind, row, col) {
            // 鼠标/触摸已在 pointerup 提交矩形；保留键盘 Enter/Space 的单格操作。
            if (event.detail === 0) paint(kind, row, col);
        }
        function typeInfo(kind, value) {
            // 游戏已有的 None 格子仍可读回显示，但不再提供对应画笔。
            if (value === 'None') return { value, label: '无', en: 'None', short: '—', code: '—' };
            return types.find(item => item.value === (kind === 'rows' && value === 'Normal' ? 'Grass' : value));
        }
        return {
            draft, loading, applying, busy, dirty, brush, selection,
            types, load, apply, reset, receive,
            pointerDown, pointerMove, pointerUp, cancel, selected, cellClick, typeInfo,
        };
    }
    return { create };
})();
