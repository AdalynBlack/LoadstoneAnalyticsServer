from flask import Flask,request,json
import sqlite3

app = Flask(__name__)

@app.route('/ping')
def ping():
    return 'Pong!'

@app.route('/performance-report', methods=['POST'])
def performanceReport():
    data = request.json
    print(data)

    con = sqlite3.connect('analytics.db')
    cur = con.cursor()

    try:
        cur.execute('INSERT INTO performanceReports (moon, seed, playerCount, sceneLoadTime, sceneWaitTime, interior, mainPathRoomCount, branchPathRoomCount, totalRoomCount, maxBranchDepth, totalRetries, prunedBranchTileCount, preProcessTime, mainPathGenerationTime, branchPathGenerationTime, postProcessTime, totalDungenTime, dungenWaitTime, spawnSyncedPropsTime, generatedFloorPostProcessingTime, refreshEnemyVentsTime, finishGeneratingNewLevelTime, finishGeneratingLevelTime, totalLoadTime) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (
            data['moon'], data['seed'], data['playerCount'],
            data['sceneLoadTime'], data['sceneWaitTime'],
            data['interior'],
            data['mainPathRoomCount'], data['branchPathRoomCount'], data['totalRoomCount'],
            data['maxBranchDepth'],
            data['totalRetries'],
            data['prunedBranchTileCount'],
            data['preProcessTime'], data['mainPathGenerationTime'], data['branchPathGenerationTime'], data['postProcessTime'], data['totalDungenTime'],
            data['dungenWaitTime'],
            data['spawnSyncedPropsTime'], data['generatedFloorPostProcessingTime'], data['refreshEnemyVentsTime'], data['finishGeneratingNewLevelTime'],
            data['finishGeneratingLevelTime'],
            data['totalLoadTime']))
    except KeyError as e:
        print(e)
        con.close()
        return f'{{"response": "Invalid performance report format. Missing required key {e}"}}', 400
    con.commit()

    data['ID'] = cur.lastrowid

    con.close()
    return data

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, ssl_context=('cert.pem', 'key.pem'))
